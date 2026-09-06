import { useEffect } from "react";
import { useLeadStore } from "@/lib/leads/store";

export function LeadsHydrate() {
  useEffect(() => {
    void useLeadStore.persist.rehydrate();
  }, []);
  return null;
}
