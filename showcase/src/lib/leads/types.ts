export const SERVICE_CATEGORIES = [
  "website_development",
  "telegram_bot",
  "api_integration",
  "business_automation",
  "other",
] as const;

export const LEAD_STATUSES = [
  "new",
  "in_progress",
  "completed",
  "cancelled",
] as const;

export const CONTACT_METHODS = [
  "telegram",
  "phone",
  "email",
  "whatsapp",
] as const;

export type ServiceCategory = (typeof SERVICE_CATEGORIES)[number];
export type LeadStatus = (typeof LEAD_STATUSES)[number];
export type ContactMethod = (typeof CONTACT_METHODS)[number];

export type Lead = {
  id: number;
  publicId: string;
  telegramUserId: number;
  username: string | null;
  fullName: string;
  phone: string;
  serviceCategory: ServiceCategory;
  description: string;
  preferredContactMethod: ContactMethod;
  status: LeadStatus;
  adminNote: string | null;
  createdAt: string;
  updatedAt: string;
};

export type LeadDraft = {
  fullName: string;
  phone: string;
  serviceCategory: ServiceCategory | null;
  description: string;
  preferredContactMethod: ContactMethod | null;
};

export const CATEGORY_LABELS: Record<ServiceCategory, string> = {
  website_development: "Website development",
  telegram_bot: "Telegram bot",
  api_integration: "API integration",
  business_automation: "Business automation",
  other: "Other",
};

export const STATUS_LABELS: Record<LeadStatus, string> = {
  new: "New",
  in_progress: "In Progress",
  completed: "Completed",
  cancelled: "Cancelled",
};

export const CONTACT_LABELS: Record<ContactMethod, string> = {
  telegram: "Telegram",
  phone: "Phone",
  email: "Email",
  whatsapp: "WhatsApp",
};
