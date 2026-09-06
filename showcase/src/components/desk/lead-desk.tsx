import { useMemo, useState } from "react";
import { Download, RotateCcw } from "lucide-react";
import { toast } from "sonner";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Sheet, SheetContent } from "@/components/ui/sheet";
import { Textarea } from "@/components/ui/textarea";
import { downloadCsv } from "@/lib/leads/csv";
import { BOT_COPY } from "@/lib/leads/copy";
import { statsFrom, useLeadStore } from "@/lib/leads/store";
import { STATUS_BADGE } from "@/lib/leads/status-style";
import {
  CATEGORY_LABELS,
  CONTACT_LABELS,
  LEAD_STATUSES,
  STATUS_LABELS,
  type Lead,
  type LeadStatus,
} from "@/lib/leads/types";
import { cn } from "@/lib/utils";

function formatStamp(iso: string) {
  return new Date(iso).toLocaleString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    timeZone: "UTC",
  });
}

export function LeadDesk() {
  const leads = useLeadStore((s) => s.leads);
  const updateStatus = useLeadStore((s) => s.updateStatus);
  const updateNote = useLeadStore((s) => s.updateNote);
  const resetDemo = useLeadStore((s) => s.resetDemo);
  const [filter, setFilter] = useState<LeadStatus | "all">("all");
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [note, setNote] = useState("");
  const [notify, setNotify] = useState(true);

  const stats = statsFrom(leads);
  const selected = leads.find((lead) => lead.id === selectedId) ?? null;

  const visible = useMemo(() => {
    const list =
      filter === "all" ? leads : leads.filter((lead) => lead.status === filter);
    return [...list].sort((a, b) => b.createdAt.localeCompare(a.createdAt));
  }, [leads, filter]);

  function openLead(lead: Lead) {
    setSelectedId(lead.id);
    setNote(lead.adminNote ?? "");
  }

  function changeStatus(status: LeadStatus) {
    if (!selected) return;
    const previous = selected.status;
    const updated = updateStatus(selected.id, status);
    if (!updated) return;
    if (notify && previous !== status) {
      toast.message("Customer notified", {
        description: BOT_COPY.statusNotice(
          updated.publicId,
          STATUS_LABELS[status],
        ),
      });
    } else if (previous === status) {
      toast.message("Status unchanged");
    } else {
      toast.success(`Moved ${updated.publicId} to ${STATUS_LABELS[status]}`);
    }
  }

  function saveNote() {
    if (!selected) return;
    updateNote(selected.id, note);
    toast.success("Internal note saved");
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-3 lg:grid-cols-5">
        <Stat label="Total" value={stats.total} />
        <Stat label="New" value={stats.new} />
        <Stat label="In progress" value={stats.in_progress} />
        <Stat label="Completed" value={stats.completed} />
        <Stat label="Cancelled" value={stats.cancelled} />
      </div>

      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex flex-wrap gap-1.5">
          <FilterChip
            active={filter === "all"}
            onClick={() => setFilter("all")}
            label="All"
          />
          {LEAD_STATUSES.map((status) => (
            <FilterChip
              key={status}
              active={filter === status}
              onClick={() => setFilter(status)}
              label={STATUS_LABELS[status]}
            />
          ))}
        </div>
        <div className="flex flex-wrap gap-2">
          <Button
            variant="secondary"
            onClick={() => {
              downloadCsv(leads);
              toast.success("CSV exported");
            }}
          >
            <Download />
            Export CSV
          </Button>
          <Button
            variant="ghost"
            onClick={() => {
              resetDemo();
              setSelectedId(null);
              toast.message("Sample leads restored");
            }}
          >
            <RotateCcw />
            Reset sample data
          </Button>
        </div>
      </div>

      <Card className="overflow-hidden p-0">
        <div className="hidden grid-cols-[140px_1fr_140px_120px_120px] gap-3 border-b border-border px-4 py-3 text-xs tracking-wide text-muted uppercase md:grid">
          <span>Lead</span>
          <span>Customer</span>
          <span>Service</span>
          <span>Status</span>
          <span>Created</span>
        </div>
        <ul>
          {visible.map((lead) => (
            <li key={lead.id} className="border-b border-border last:border-0">
              <button
                type="button"
                onClick={() => openLead(lead)}
                className="grid w-full min-h-14 grid-cols-1 gap-1 px-4 py-3 text-left transition-colors duration-150 hover:bg-elevated/70 md:grid-cols-[140px_1fr_140px_120px_120px] md:items-center md:gap-3"
              >
                <span className="font-mono text-xs text-primary">
                  {lead.publicId}
                </span>
                <span className="truncate text-sm">
                  {lead.fullName}
                  <span className="mt-0.5 block text-xs text-muted md:inline md:ml-2">
                    {lead.phone}
                  </span>
                </span>
                <span className="text-sm text-muted">
                  {CATEGORY_LABELS[lead.serviceCategory]}
                </span>
                <span>
                  <Badge variant={STATUS_BADGE[lead.status]}>
                    {STATUS_LABELS[lead.status]}
                  </Badge>
                </span>
                <span className="font-mono text-xs text-muted tabular-nums">
                  {formatStamp(lead.createdAt)}
                </span>
              </button>
            </li>
          ))}
        </ul>
        {visible.length === 0 ? (
          <p className="px-4 py-10 text-center text-sm text-muted">
            No leads in this view.
          </p>
        ) : null}
      </Card>

      <Sheet
        open={selectedId !== null}
        onOpenChange={(open) => {
          if (!open) setSelectedId(null);
        }}
      >
        <SheetContent title={selected?.publicId ?? "Lead"}>
          {selected ? (
            <div className="space-y-6">
              <div>
                <h2 className="font-display text-2xl italic">
                  {selected.fullName}
                </h2>
                <p className="mt-1 text-sm text-muted">
                  @{selected.username ?? "unknown"} · {selected.telegramUserId}
                </p>
              </div>
              <dl className="grid grid-cols-1 gap-3 text-sm">
                <Row label="Phone" value={selected.phone} />
                <Row
                  label="Service"
                  value={CATEGORY_LABELS[selected.serviceCategory]}
                />
                <Row
                  label="Contact"
                  value={CONTACT_LABELS[selected.preferredContactMethod]}
                />
                <Row label="Created" value={formatStamp(selected.createdAt)} />
                <Row label="Updated" value={formatStamp(selected.updatedAt)} />
              </dl>
              <div>
                <p className="mb-2 text-xs tracking-wide text-muted uppercase">
                  Project brief
                </p>
                <p className="rounded-lg bg-elevated p-3 text-sm leading-relaxed">
                  {selected.description}
                </p>
              </div>
              <div>
                <p className="mb-2 text-xs tracking-wide text-muted uppercase">
                  Status
                </p>
                <div className="grid grid-cols-2 gap-2">
                  {LEAD_STATUSES.map((status) => (
                    <Button
                      key={status}
                      variant={
                        selected.status === status ? "default" : "secondary"
                      }
                      onClick={() => changeStatus(status)}
                    >
                      {STATUS_LABELS[status]}
                    </Button>
                  ))}
                </div>
                <label className="mt-3 flex min-h-11 items-center gap-2 text-sm text-muted">
                  <input
                    type="checkbox"
                    checked={notify}
                    onChange={(event) => setNotify(event.target.checked)}
                    className="size-4 accent-primary"
                  />
                  Notify customer when status changes
                </label>
              </div>
              <div className="space-y-2">
                <Label htmlFor="admin-note">Internal note</Label>
                <Textarea
                  id="admin-note"
                  value={note}
                  onChange={(event) => setNote(event.target.value)}
                  placeholder="Visible only to administrators"
                />
                <Button onClick={saveNote}>Save note</Button>
              </div>
            </div>
          ) : null}
        </SheetContent>
      </Sheet>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: number }) {
  return (
    <Card className="p-4">
      <p className="text-xs tracking-wide text-muted uppercase">{label}</p>
      <p className="mt-2 font-display text-3xl italic tabular-nums">{value}</p>
    </Card>
  );
}

function FilterChip({
  active,
  label,
  onClick,
}: {
  active: boolean;
  label: string;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        "min-h-11 rounded-full px-3.5 text-sm transition-colors duration-150",
        active
          ? "bg-primary text-primary-fg"
          : "bg-elevated text-muted hover:text-fg",
      )}
    >
      {label}
    </button>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-baseline justify-between gap-4 border-b border-border py-2">
      <dt className="text-muted">{label}</dt>
      <dd className="text-right">{value}</dd>
    </div>
  );
}
