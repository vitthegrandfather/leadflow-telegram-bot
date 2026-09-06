const NAME_RE = /^[\p{L}][\p{L}\s.'-]{1,79}$/u;

export function normalizePhone(raw: string): string {
  const trimmed = raw.trim();
  let value = trimmed.replace(/[^\d+]/g, "");
  if (value.startsWith("00")) {
    value = `+${value.slice(2)}`;
  }
  const digits = value.replace(/\D/g, "");
  if (digits.length < 8 || digits.length > 15) {
    throw new Error("Enter a phone number with 8 to 15 digits.");
  }
  return `+${digits}`;
}

export function validateName(raw: string): string {
  const name = raw.trim().replace(/\s+/g, " ");
  if (!NAME_RE.test(name)) {
    throw new Error("Enter a full name using 2–80 letters.");
  }
  return name;
}

export function validateDescription(raw: string): string {
  const text = raw.trim();
  if (text.length < 10) {
    throw new Error("Describe the project in at least 10 characters.");
  }
  if (text.length > 1000) {
    throw new Error("Keep the description under 1,000 characters.");
  }
  return text;
}

export function generatePublicId(date = new Date()): string {
  const stamp = date.toISOString().slice(2, 10).replaceAll("-", "");
  const bytes = new Uint8Array(2);
  crypto.getRandomValues(bytes);
  const suffix = Array.from(bytes, (b) => b.toString(16).padStart(2, "0"))
    .join("")
    .toUpperCase();
  return `LF-${stamp}-${suffix}`;
}
