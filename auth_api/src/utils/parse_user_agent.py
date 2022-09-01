from user_agents import parse
from core.constants import DeviceTypes


def get_device_type(user_agent: str) -> str:
    user_agent = parse(user_agent)
    if user_agent.is_pc:
        return DeviceTypes.PC.value
    if user_agent.is_mobile or user_agent.is_tablet:
        return DeviceTypes.MOBILE.value
    return DeviceTypes.OTHER.value
