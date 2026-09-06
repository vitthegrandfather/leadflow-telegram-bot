import { useEffect, useMemo, useRef, useState } from "react";
import { Send } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PhoneFrame } from "@/components/telegram/phone-frame";
import { BOT_COPY } from "@/lib/leads/copy";
import {
  CATEGORY_LABELS,
  CONTACT_LABELS,
  CONTACT_METHODS,
  SERVICE_CATEGORIES,
  STATUS_LABELS,
  type ContactMethod,
  type LeadDraft,
  type ServiceCategory,
} from "@/lib/leads/types";
import {
  DuplicateLeadError,
  useLeadStore,
} from "@/lib/leads/store";
import {
  normalizePhone,
  validateDescription,
  validateName,
} from "@/lib/leads/validation";
import { DEMO_VIEWER_USER_ID } from "@/lib/leads/seed";
import { cn } from "@/lib/utils";

type Step =
  | "menu"
  | "name"
  | "phone"
  | "category"
  | "description"
  | "contact"
  | "confirm"
  | "edit"
  | "requests"
  | "about";

type ChatMessage = {
  id: string;
  from: "bot" | "user";
  text: string;
};

type InlineButton = { id: string; label: string };

const emptyDraft: LeadDraft = {
  fullName: "",
  phone: "",
  serviceCategory: null,
  description: "",
  preferredContactMethod: null,
};

function summaryText(draft: LeadDraft): string {
  return [
    "Please confirm this request:",
    `Name: ${draft.fullName}`,
    `Phone: ${draft.phone}`,
    `Service: ${draft.serviceCategory ? CATEGORY_LABELS[draft.serviceCategory] : "—"}`,
    `Contact: ${draft.preferredContactMethod ? CONTACT_LABELS[draft.preferredContactMethod] : "—"}`,
    `Brief: ${draft.description}`,
  ].join("\n");
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    timeZone: "UTC",
  });
}

export function ChatDemo({ compact = false }: { compact?: boolean }) {
  const [step, setStep] = useState<Step>("menu");
  const [draft, setDraft] = useState<LeadDraft>(emptyDraft);
  const [input, setInput] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([
    { id: "m0", from: "bot", text: BOT_COPY.welcome },
  ]);
  const scroller = useRef<HTMLDivElement>(null);
  const listForUser = useLeadStore((s) => s.listForUser);
  const createLead = useLeadStore((s) => s.createLead);
  const leads = useLeadStore((s) => s.leads);

  const myLeads = useMemo(
    () => listForUser(DEMO_VIEWER_USER_ID),
    [listForUser, leads],
  );

  useEffect(() => {
    scroller.current?.scrollTo({
      top: scroller.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages, step]);

  function push(from: ChatMessage["from"], text: string) {
    setMessages((current) => [
      ...current,
      { id: `${Date.now()}-${current.length}`, from, text },
    ]);
  }

  function goMenu() {
    setStep("menu");
    setDraft(emptyDraft);
    setInput("");
    setError(null);
  }

  function handleInline(id: string) {
    setError(null);
    if (id === "submit") {
      push("user", "Submit a request");
      push("bot", BOT_COPY.askName);
      setStep("name");
      return;
    }
    if (id === "requests") {
      push("user", "My requests");
      if (myLeads.length === 0) {
        push("bot", BOT_COPY.emptyRequests);
      } else {
        const lines = myLeads
          .slice(0, 8)
          .map(
            (lead) =>
              `${lead.publicId} · ${CATEGORY_LABELS[lead.serviceCategory]} · ${STATUS_LABELS[lead.status]} · ${formatDate(lead.createdAt)}`,
          );
        push("bot", lines.join("\n"));
      }
      setStep("requests");
      return;
    }
    if (id === "about") {
      push("user", "About");
      push("bot", BOT_COPY.about);
      setStep("about");
      return;
    }
    if (id === "home") {
      push("user", "Main menu");
      push("bot", BOT_COPY.welcome);
      goMenu();
      return;
    }
    if (id.startsWith("cat:")) {
      const value = id.slice(4) as ServiceCategory;
      const next = { ...draft, serviceCategory: value };
      setDraft(next);
      push("user", CATEGORY_LABELS[value]);
      if (next.description) {
        push("bot", summaryText(next));
        setStep("confirm");
      } else {
        push("bot", BOT_COPY.askDescription);
        setStep("description");
      }
      return;
    }
    if (id.startsWith("cm:")) {
      const value = id.slice(3) as ContactMethod;
      const next = { ...draft, preferredContactMethod: value };
      setDraft(next);
      push("user", CONTACT_LABELS[value]);
      push("bot", summaryText(next));
      setStep("confirm");
      return;
    }
    if (id === "confirm") {
      push("user", "Confirm");
      try {
        const lead = createLead(draft);
        push("bot", BOT_COPY.success(lead.publicId));
        goMenu();
      } catch (err) {
        if (err instanceof DuplicateLeadError) {
          push("bot", BOT_COPY.duplicate(err.lead.publicId));
          goMenu();
          return;
        }
        setError(err instanceof Error ? err.message : "Could not save.");
      }
      return;
    }
    if (id === "edit") {
      push("user", "Edit");
      push("bot", "Which field should I change?");
      setStep("edit");
      return;
    }
    if (id === "cancel") {
      push("user", "Cancel");
      push("bot", BOT_COPY.cancelled);
      goMenu();
      return;
    }
    if (id.startsWith("edit:")) {
      const field = id.slice(5);
      if (field === "name") {
        push("bot", BOT_COPY.askName);
        setStep("name");
      } else if (field === "phone") {
        push("bot", BOT_COPY.askPhone);
        setStep("phone");
      } else if (field === "category") {
        push("bot", BOT_COPY.askCategory);
        setStep("category");
      } else if (field === "description") {
        push("bot", BOT_COPY.askDescription);
        setStep("description");
      } else if (field === "contact") {
        push("bot", BOT_COPY.askContact);
        setStep("contact");
      }
    }
  }

  function submitText() {
    const value = input.trim();
    if (!value) return;
    setError(null);
    try {
      if (step === "name") {
        const name = validateName(value);
        setDraft((d) => ({ ...d, fullName: name }));
        push("user", name);
        setInput("");
        if (draft.phone) {
          push("bot", summaryText({ ...draft, fullName: name }));
          setStep("confirm");
        } else {
          push("bot", BOT_COPY.askPhone);
          setStep("phone");
        }
        return;
      }
      if (step === "phone") {
        const phone = normalizePhone(value);
        setDraft((d) => ({ ...d, phone }));
        push("user", phone);
        setInput("");
        if (draft.serviceCategory && draft.description) {
          push("bot", summaryText({ ...draft, phone }));
          setStep("confirm");
        } else {
          push("bot", BOT_COPY.askCategory);
          setStep("category");
        }
        return;
      }
      if (step === "description") {
        const description = validateDescription(value);
        setDraft((d) => ({ ...d, description }));
        push("user", description);
        setInput("");
        if (draft.preferredContactMethod) {
          push("bot", summaryText({ ...draft, description }));
          setStep("confirm");
        } else {
          push("bot", BOT_COPY.askContact);
          setStep("contact");
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Please try again.");
    }
  }

  const awaitingText = step === "name" || step === "phone" || step === "description";

  const buttons: InlineButton[] = (() => {
    if (step === "menu" || step === "requests" || step === "about") {
      return [
        { id: "submit", label: "Submit a request" },
        { id: "requests", label: "My requests" },
        { id: "about", label: "About" },
      ];
    }
    if (step === "category") {
      return SERVICE_CATEGORIES.map((id) => ({
        id: `cat:${id}`,
        label: CATEGORY_LABELS[id],
      }));
    }
    if (step === "contact") {
      return CONTACT_METHODS.map((id) => ({
        id: `cm:${id}`,
        label: CONTACT_LABELS[id],
      }));
    }
    if (step === "confirm") {
      return [
        { id: "confirm", label: "Confirm" },
        { id: "edit", label: "Edit" },
        { id: "cancel", label: "Cancel" },
      ];
    }
    if (step === "edit") {
      return [
        { id: "edit:name", label: "Name" },
        { id: "edit:phone", label: "Phone" },
        { id: "edit:category", label: "Service" },
        { id: "edit:description", label: "Brief" },
        { id: "edit:contact", label: "Contact" },
        { id: "cancel", label: "Cancel" },
      ];
    }
    return [{ id: "cancel", label: "Cancel" }];
  })();

  return (
    <PhoneFrame>
      <div
        className={cn(
          "flex flex-col bg-surface",
          compact ? "h-[520px]" : "h-[640px] sm:h-[680px]",
        )}
      >
        <div className="flex items-center gap-3 border-b border-border px-3 py-2.5">
          <span className="inline-flex size-9 items-center justify-center rounded-full bg-primary font-display text-sm text-primary-fg italic">
            Lf
          </span>
          <div className="min-w-0">
            <p className="truncate text-sm font-medium">LeadFlow Bot</p>
            <p className="text-xs text-ok">demo · not a live client bot</p>
          </div>
        </div>
        <div
          ref={scroller}
          className="flex-1 space-y-2 overflow-y-auto px-3 py-3"
        >
          {messages.map((message) => (
            <div
              key={message.id}
              className={cn(
                "max-w-[85%] rounded-lg px-3 py-2 text-sm leading-relaxed whitespace-pre-wrap",
                message.from === "bot"
                  ? "rounded-tl-xs bg-elevated text-fg"
                  : "ml-auto rounded-tr-xs bg-primary text-primary-fg",
              )}
            >
              {message.text}
            </div>
          ))}
          <div className="grid grid-cols-1 gap-1.5 pt-1">
            {buttons.map((button) => (
              <button
                key={button.id}
                type="button"
                onClick={() => handleInline(button.id)}
                className="min-h-11 rounded-md border border-border bg-bg px-3 py-2 text-left text-sm text-fg transition-colors duration-150 hover:border-primary/50 hover:text-primary"
              >
                {button.label}
              </button>
            ))}
          </div>
        </div>
        <form
          className="border-t border-border p-2.5"
          onSubmit={(event) => {
            event.preventDefault();
            submitText();
          }}
        >
          {error ? (
            <p className="mb-2 px-1 text-xs text-danger">{error}</p>
          ) : null}
          <div className="flex items-center gap-2">
            <input
              value={input}
              onChange={(event) => setInput(event.target.value)}
              disabled={!awaitingText}
              placeholder={
                awaitingText ? "Write a message" : "Choose an option above"
              }
              className="h-11 flex-1 rounded-md border border-border bg-bg px-3 text-sm text-fg placeholder:text-subtle focus-visible:ring-2 focus-visible:ring-ring/70 focus-visible:outline-none disabled:opacity-50"
            />
            <Button
              type="submit"
              size="icon"
              disabled={!awaitingText || !input.trim()}
              aria-label="Send"
            >
              <Send className="size-4" />
            </Button>
          </div>
        </form>
      </div>
    </PhoneFrame>
  );
}
