import { create } from "zustand";
import { persist } from "zustand/middleware";
import { SEED_LEADS, DEMO_VIEWER_USER_ID } from "./seed";
import { generatePublicId } from "./validation";
import type { Lead, LeadDraft, LeadStatus } from "./types";

const DUPLICATE_WINDOW_MS = 10 * 60 * 1000;

type LeadStore = {
  leads: Lead[];
  nextId: number;
  createLead: (draft: LeadDraft, telegramUserId?: number) => Lead;
  listForUser: (telegramUserId: number) => Lead[];
  findDuplicate: (draft: LeadDraft, telegramUserId: number) => Lead | null;
  updateStatus: (id: number, status: LeadStatus) => Lead | null;
  updateNote: (id: number, note: string) => Lead | null;
  resetDemo: () => void;
};

function nowIso() {
  return new Date().toISOString();
}

export const useLeadStore = create<LeadStore>()(
  persist(
    (set, get) => ({
      leads: SEED_LEADS,
      nextId: SEED_LEADS.length + 1,
      createLead: (draft, telegramUserId = DEMO_VIEWER_USER_ID) => {
        if (
          !draft.serviceCategory ||
          !draft.preferredContactMethod ||
          !draft.fullName ||
          !draft.phone
        ) {
          throw new Error("Complete every field before submitting.");
        }
        const duplicate = get().findDuplicate(draft, telegramUserId);
        if (duplicate) {
          throw new DuplicateLeadError(duplicate);
        }
        const createdAt = nowIso();
        const lead: Lead = {
          id: get().nextId,
          publicId: generatePublicId(),
          telegramUserId,
          username: "demo.customer",
          fullName: draft.fullName,
          phone: draft.phone,
          serviceCategory: draft.serviceCategory,
          description: draft.description,
          preferredContactMethod: draft.preferredContactMethod,
          status: "new",
          adminNote: null,
          createdAt,
          updatedAt: createdAt,
        };
        set({ leads: [lead, ...get().leads], nextId: lead.id + 1 });
        return lead;
      },
      listForUser: (telegramUserId) =>
        get()
          .leads.filter((lead) => lead.telegramUserId === telegramUserId)
          .sort((a, b) => b.createdAt.localeCompare(a.createdAt)),
      findDuplicate: (draft, telegramUserId) => {
        const cutoff = Date.now() - DUPLICATE_WINDOW_MS;
        return (
          get().leads.find(
            (lead) =>
              lead.telegramUserId === telegramUserId &&
              lead.phone === draft.phone &&
              lead.serviceCategory === draft.serviceCategory &&
              lead.description === draft.description &&
              new Date(lead.createdAt).getTime() >= cutoff,
          ) ?? null
        );
      },
      updateStatus: (id, status) => {
        const current = get().leads.find((lead) => lead.id === id);
        if (!current) return null;
        if (current.status === status) return current;
        const updated = { ...current, status, updatedAt: nowIso() };
        set({
          leads: get().leads.map((lead) => (lead.id === id ? updated : lead)),
        });
        return updated;
      },
      updateNote: (id, note) => {
        const current = get().leads.find((lead) => lead.id === id);
        if (!current) return null;
        const updated = {
          ...current,
          adminNote: note.trim() || null,
          updatedAt: nowIso(),
        };
        set({
          leads: get().leads.map((lead) => (lead.id === id ? updated : lead)),
        });
        return updated;
      },
      resetDemo: () => set({ leads: SEED_LEADS, nextId: SEED_LEADS.length + 1 }),
    }),
    {
      name: "leadflow-demo-leads",
      skipHydration: true,
      partialize: (state) => ({ leads: state.leads, nextId: state.nextId }),
    },
  ),
);

export class DuplicateLeadError extends Error {
  lead: Lead;
  constructor(lead: Lead) {
    super(`A matching request already exists: ${lead.publicId}`);
    this.name = "DuplicateLeadError";
    this.lead = lead;
  }
}

export function statsFrom(leads: Lead[]) {
  return {
    total: leads.length,
    new: leads.filter((l) => l.status === "new").length,
    in_progress: leads.filter((l) => l.status === "in_progress").length,
    completed: leads.filter((l) => l.status === "completed").length,
    cancelled: leads.filter((l) => l.status === "cancelled").length,
  };
}
