import { Link, useRouterState } from "@tanstack/react-router";
import type { ReactNode } from "react";
import { LeadsHydrate } from "@/components/layout/leads-hydrate";
import { cn } from "@/lib/utils";

const LINKS = [
  { to: "/", label: "Overview" },
  { to: "/demo", label: "Customer flow" },
  { to: "/desk", label: "Admin desk" },
  { to: "/architecture", label: "Architecture" },
] as const;

export function SiteHeader() {
  const pathname = useRouterState({ select: (s) => s.location.pathname });

  return (
    <header className="sticky top-0 z-30 border-b border-border/80 bg-bg/85 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between gap-4 px-4 sm:px-6">
        <Link to="/" className="flex items-center gap-2.5">
          <span className="inline-flex size-8 items-center justify-center rounded-sm bg-primary text-primary-fg">
            <svg viewBox="0 0 24 24" className="size-4" aria-hidden="true">
              <path
                fill="currentColor"
                d="M4 12.5 10 5l3.2 4.2L20 4v6.2L13.2 16 10 11.8 4 18.5z"
              />
            </svg>
          </span>
          <span className="font-display text-xl tracking-tight text-fg italic">
            LeadFlow
          </span>
        </Link>
        <nav className="flex items-center gap-1 overflow-x-auto">
          {LINKS.map((link) => {
            const active =
              link.to === "/"
                ? pathname === "/"
                : pathname.startsWith(link.to);
            return (
              <Link
                key={link.to}
                to={link.to}
                className={cn(
                  "rounded-md px-3 py-2 text-sm whitespace-nowrap transition-colors duration-150",
                  active
                    ? "bg-elevated text-fg"
                    : "text-muted hover:bg-elevated/70 hover:text-fg",
                )}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}

export function SiteFooter() {
  return (
    <footer className="border-t border-border">
      <div className="mx-auto flex max-w-6xl flex-col gap-2 px-4 py-8 text-sm text-muted sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <p>LeadFlow Bot — personal portfolio demonstration, not client work.</p>
        <p className="font-mono text-xs tracking-wide">DEMO · aiogram 3</p>
      </div>
    </footer>
  );
}

export function PageShell({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen flex-col bg-bg text-fg">
      <LeadsHydrate />
      <SiteHeader />
      <main className="flex-1">{children}</main>
      <SiteFooter />
    </div>
  );
}
