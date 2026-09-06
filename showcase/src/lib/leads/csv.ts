import {
  CATEGORY_LABELS,
  CONTACT_LABELS,
  STATUS_LABELS,
  type Lead,
} from "./types";

const HEADERS = [
  "public_id",
  "created_at",
  "status",
  "full_name",
  "phone",
  "username",
  "telegram_user_id",
  "category",
  "contact_method",
  "description",
  "admin_note",
] as const;

function csvCell(value: string): string {
  if (/[",\n]/.test(value)) {
    return `"${value.replaceAll('"', '""')}"`;
  }
  return value;
}

export function leadsToCsv(leads: Lead[]): string {
  const lines = [
    HEADERS.join(","),
    ...leads.map((lead) =>
      [
        lead.publicId,
        lead.createdAt,
        STATUS_LABELS[lead.status],
        lead.fullName,
        lead.phone,
        lead.username ?? "",
        String(lead.telegramUserId),
        CATEGORY_LABELS[lead.serviceCategory],
        CONTACT_LABELS[lead.preferredContactMethod],
        lead.description,
        lead.adminNote ?? "",
      ]
        .map(csvCell)
        .join(","),
    ),
  ];
  return `\uFEFF${lines.join("\n")}\n`;
}

export function downloadCsv(leads: Lead[], filename = "leadflow-leads.csv") {
  const blob = new Blob([leadsToCsv(leads)], {
    type: "text/csv;charset=utf-8;",
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}
