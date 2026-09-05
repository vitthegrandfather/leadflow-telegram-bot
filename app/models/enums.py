from enum import Enum


class ServiceCategory(str, Enum):
    WEBSITE_DEVELOPMENT = "website_development"
    TELEGRAM_BOT = "telegram_bot"
    API_INTEGRATION = "api_integration"
    BUSINESS_AUTOMATION = "business_automation"
    OTHER = "other"

    @property
    def label(self) -> str:
        return {
            ServiceCategory.WEBSITE_DEVELOPMENT: "Website development",
            ServiceCategory.TELEGRAM_BOT: "Telegram bot",
            ServiceCategory.API_INTEGRATION: "API integration",
            ServiceCategory.BUSINESS_AUTOMATION: "Business automation",
            ServiceCategory.OTHER: "Other",
        }[self]


class LeadStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    @property
    def label(self) -> str:
        return {
            LeadStatus.NEW: "New",
            LeadStatus.IN_PROGRESS: "In Progress",
            LeadStatus.COMPLETED: "Completed",
            LeadStatus.CANCELLED: "Cancelled",
        }[self]


class ContactMethod(str, Enum):
    TELEGRAM = "telegram"
    PHONE = "phone"
    EMAIL = "email"
    WHATSAPP = "whatsapp"

    @property
    def label(self) -> str:
        return {
            ContactMethod.TELEGRAM: "Telegram",
            ContactMethod.PHONE: "Phone",
            ContactMethod.EMAIL: "Email",
            ContactMethod.WHATSAPP: "WhatsApp",
        }[self]
