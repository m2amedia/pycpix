"""
CPIX stuff
"""
import uuid
from lxml import etree
from base64 import b64decode
from binascii import Error as BinasciiError


VALID_SYSTEM_IDS = [
    uuid.UUID("1077efec-c0b2-4d02-ace3-3c1e52e2fb4b"),  # org.w3.clearkey
    uuid.UUID("9a04f079-9840-4286-ab92-e65be0885f95"),  # Microsoft Playready
    uuid.UUID("F239E769-EFA3-4850-9C16-A903C6932EFB"),  # Adobe Primetime DRM, version 4
    uuid.UUID("5E629AF5-38DA-4063-8977-97FFBD9902D4"),  # Marlin
    uuid.UUID("9a27dd82-fde2-4725-8cbc-4234aa06ec09"),  # Verimatrix
    uuid.UUID("edef8ba9-79d6-4ace-a3c8-27dcd51d21ed"),  # Widevine
    uuid.UUID("80a6be7e-1448-4c37-9e70-d5aebe04c8d2"),  # Irdeto
    uuid.UUID("279fe473-512c-48fe-ade8-d176fee6b40f"),  # Latens
    uuid.UUID("B4413586-C58C-FFB0-94A5-D4896C1AF6C3"),  # Viaccess-Orca DRM (VODRM)
    uuid.UUID("94CE86FB-07FF-4F43-ADB8-93D2FA968CA2"),  # Apple FairPlay
]
PSKC = "urn:ietf:params:xml:ns:keyprov:pskc"
XSI = "http://www.w3.org/2001/XMLSchema-instance"
NSMAP = {
    None: "urn:dashif:org:cpix",
    "xsi": XSI,
    "pskc": PSKC}

def encode_bool(value):
    """Encode booleans to produce valid XML"""
    if value:
        return "true"
    return "false"


class CPIX(object):
    def __init__(self, content_keys=None, drm_systems=None, usage_rules=None):
        if content_keys is not None and not isinstance(content_keys, ContentKeyList):
            raise TypeError("content_keys should be a ContentKeyList")
        self.content_keys = content_keys
        if drm_systems is not None and not isinstance(drm_systems, DRMSystemList):
            raise TypeError("drm_systems should be a DRMSystemList")
        self.drm_systems = drm_systems
        if usage_rules is not None and not isinstance(usage_rules, UsageRuleList):
            raise TypeError("usage_rules should be a UsageRuleList")
        self.usage_rules = usage_rules
        
    def element(self):
        el = etree.Element("CPIX", nsmap=NSMAP)
        el.set("{{{xsi}}}schemaLocation".format(
            xsi=XSI), "urn:dashif:org:cpix cpix.xsd")
        if self.content_keys is not None and isinstance(self.content_keys, ContentKeyList):
            el.append(self.content_keys.element())
        if self.drm_systems is not None and isinstance(self.drm_systems, DRMSystemList):
            el.append(self.drm_systems.element())
        if self.usage_rules is not None and isinstance(self.usage_rules, UsageRuleList):
            el.append(self.usage_rules.element())
        return el


class ContentKeyList(object):
    """List of ContentKeys"""
    def __init__(self, content_keys=[]):
        if content_keys is not None and not isinstance(content_keys, list) and not all(isinstance(x, ContentKey) for x in content_keys):
            raise TypeError(
                "content_keys should be a list of ContentKeys")
        self.content_keys = content_keys

    def __len__(self):
        return len(self.content_keys)

    def element(self):
        el = etree.Element("ContentKeyList", nsmap=NSMAP)
        for content_key in self.content_keys:
            el.append(content_key.element())
        return el


class ContentKey(object):
    """
    ContentKey element
    Has required attribute:
        kid: key ID
    And child element:
        Data: data element containing content encryption key
    """
    def __init__(self, kid, cek):
        if kid is not None and not isinstance(kid, (str, uuid.UUID)):
            raise TypeError("kid should be a uuid")
        self.kid = uuid.UUID(kid)
        if cek is not None and not isinstance(cek, str):
            raise TypeError("cek should be a string")
        try:
            b64decode(cek)
        except BinasciiError:
            raise ValueError("cek is not a valid base64 string")
            
        self.cek = cek
    
    def element(self):
        """Returns XML element"""
        el = etree.Element("ContentKey", nsmap=NSMAP)
        el.set("kid", str(self.kid))
        data = etree.SubElement(el, "Data", nsmap=NSMAP)
        secret = etree.SubElement(
            data, "{{{pskc}}}Secret".format(pskc=PSKC), nsmap=NSMAP)
        plain_value = etree.SubElement(
            secret, "{{{pskc}}}PlainValue".format(pskc=PSKC), nsmap=NSMAP)
        plain_value.text = self.cek
        return el
        

class DRMSystemList(object):
    """List of DRMSystems"""
    def __init__(self, drm_systems=[]):
        if drm_systems is not None and not isinstance(drm_systems, list) and not all(isinstance(x, DRMSystem) for x in drm_systems):
            raise TypeError(
                "drm_systems should be a list of DRMSystems")
        self.drm_systems = drm_systems

    def __len__(self):
        return len(self.drm_systems)

    def element(self):
        el = etree.Element("DRMSystemList")
        for drm_system in self.drm_systems:
            el.append(drm_system.element())
        return el


class DRMSystem(object):
    """
    DRMSystem element
    Has required attributes:
        kid: key ID
        systemId: DRM system ID
    And optional child elements depending on context (all are base64 encoded):
        PSSH: PSSH box for insertion in ISOBMFF output
        ContentProtectionData: ContentProtection XML for DASH manifest
        HLSSignalingData: Signalling information for HLS manifest
    """
    def __init__(self, kid, system_id=None, pssh=None,
                 content_protection_data=None, hls_signalling_data=None):
        if kid is not None and not isinstance(kid, (str, uuid.UUID)):
            raise TypeError("kid should be a uuid")
        self.kid = uuid.UUID(kid)
        if system_id is not None and not isinstance(system_id, (str, uuid.UUID)):
            raise TypeError("system_id should be a uuid")
        if system_id is not None and uuid.UUID(system_id) not in VALID_SYSTEM_IDS:
            raise ValueError("system_id is unknown")
        self.system_id=uuid.UUID(system_id)
        if pssh is not None and not isinstance(pssh, str):
            raise TypeError("pssh should be a string")
        self.pssh = pssh
        if content_protection_data is not None and not isinstance(content_protection_data, str):
            raise TypeError("content_protection_data should be a string")
        self.content_protection_data = content_protection_data
        if hls_signalling_data is not None and not isinstance(hls_signalling_data, str):
            raise TypeError("hls_signalling_data should be a string")
        self.hls_signalling_data = hls_signalling_data

    def element(self):
        """Returns XML element"""
        el = etree.Element("DRMSystem")
        if self.kid is not None:
            el.set("kid", str(self.kid))
        if self.system_id is not None:
            el.set("systemId", str(self.system_id))
        if self.pssh is not None:
            pssh_element = etree.Element("PSSH")
            pssh_element.text = self.pssh
            el.append(pssh_element)
        if self.content_protection_data is not None:
            cpd_element = etree.Element("ContentProtectionData")
            cpd_element.text = self.content_protection_data
            el.append(cpd_element)
        if self.hls_signalling_data is not None:
            hls_element = etree.Element("HLSSignalingData")
            hls_element.text = self.hls_signalling_data
            el.append(hls_element)
        return el


class UsageRuleList(object):
    """List of UsageRules"""
    def __init__(self, usage_rules=[]):
        if usage_rules is not None and not isinstance(usage_rules, list) and not all(isinstance(x, UsageRule) for x in usage_rules):
            raise TypeError(
                "usage_rules should be a list of UsageRules")
        self.usage_rules = usage_rules

    def __len__(self):
        return len(self.usage_rules)

    def element(self):
        el = etree.Element("ContentKeyUsageRuleList")
        for usage_rule in self.usage_rules:
            el.append(usage_rule.element())
        return el


class UsageRule(object):
    """
    ContentKeyUsageRule element
    Has required attributes:
        kid: key ID to which this rule applies
    And optional child elements:
        KeyPeriodFilter: time based filters for key rotation (not currently supported by USP)
        LabelFilter: label based filters (not currently supported by USP)
        VideoFilter: video based filters
        AudioFilter: audio based filters
        BitrateFilter: bitrate based filters
    """
    def __init__(self, kid, filters=[]):
        if kid is not None and not isinstance(kid, str):
            raise TypeError("kid should be a string")
        self.kid = kid

        if filters is not None and not isinstance(filters, list) and not all(isinstance(x, (PeriodFilter, LabelFilter, AudioFilter, VideoFilter, BitrateFilter)) for x in filters):
            raise TypeError(
                "filters should be a list of filters (PeriodFilter, LabelFilter, AudioFilter, VideoFilter, BitrateFilter)")
        self.filters = filters

    def __len__(self):
        return len(self.filters)

    def element(self):
        """Returns XML element"""
        el = etree.Element("ContentKeyUsageRule")
        if self.kid is not None:
            el.set("kid", str(self.kid))
        for filter in self.filters:
            el.append(filter.element())
        return el


class PeriodFilter(object):
    """
    PeriodFilter element
    Not yet implemented
    """


class LabelFilter(object):
    """
    LabelFilter element
    Not yet implemented
    """


class VideoFilter(object):
    """
    VideoFilter element
    Has optional attributes:
        minPixels
        maxPixels
        hdr
        wcg
        minFps
        maxFps
    """
    def __init__(self, min_pixels=None, max_pixels=None, hdr=None, wcg=None,
                 min_fps=None, max_fps=None):
        self.min_pixels = min_pixels
        self.max_pixels = max_pixels
        self.hdr = hdr
        self.wcg = wcg
        self.min_fps = min_fps
        self.max_fps = max_fps
    
    def element(self):
        """Returns XML element"""
        el = etree.Element("VideoFilter")
        if self.min_pixels is not None:
            el.set("minPixels", str(self.min_pixels))
        if self.max_pixels is not None:
            el.set("maxPixels", str(self.max_pixels))
        if self.hdr is not None:
            el.set("hdr", encode_bool(self.hdr))
        if self.wcg is not None:
            el.set("wcg", encode_bool(self.wcg))
        if self.min_fps is not None:
            el.set("minFps", str(self.min_fps))
        if self.max_fps is not None:
            el.set("maxFps", str(self.max_fps))
        return el


class AudioFilter(object):
    """
    AudioFilter element
    Has optional attributes:
        minChannels
        maxChannels
    """
    def __init__(self, min_channels=None, max_channels=None):
        self.min_channels = min_channels
        self.max_channels = max_channels

    def element(self):
        """Returns XML element"""
        el = etree.Element("AudioFilter")
        if self.min_channels:
            el.set("minChannels", self.min_channels)
        if self.max_channels:
            el.set("maxChannels", self.max_channels)
        return el


class BitrateFilter(object):
    """
    BitrateFilter element
    Has optional attributes:
        minBitrate
        maxBitrate
    """
    def __init__(self, min_bitrate=None, max_bitrate=None):
        self.min_bitrate = min_bitrate
        self.max_bitrate = max_bitrate
