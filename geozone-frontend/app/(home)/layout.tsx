// import type { ReactNode } from "react";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import { AppSidebar } from "@/features/dashboard/components/app-sidebar";
import DashboardHeader from "@/features/dashboard/components/dashboard-header";

export default function DashboardLayout({ children }: LayoutProps<"/">) {
  return (
    <>
      <SidebarProvider>
        <AppSidebar />
        <SidebarInset>
          <DashboardHeader />
          <main className="min-h-screen w-full">{children}</main>
        </SidebarInset>
      </SidebarProvider>
    </>
  );
}
