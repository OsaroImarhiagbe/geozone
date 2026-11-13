import * as React from "react";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { House, FolderGit, Settings, Orbit } from "lucide-react";

const data = [
  { title: "Home", icon: House, url: "#", active: true },
  { title: "Projects", icon: FolderGit, url: "#" },
  { title: "Settings", icon: Settings, url: "#" },
];

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar {...props}>
      <SidebarHeader className="border-b border-white/10 bg-[#070C14] p-4">
        <div className="flex items-center gap-2.5">
          <div className="flex h-8 w-8 items-center justify-center rounded-md border border-cyan-400/40 bg-cyan-400/10">
            <Orbit className="h-4 w-4 text-cyan-300" />
          </div>
          <span className="font-mono text-xl font-bold tracking-tight text-slate-50">
            GeoZone
          </span>
        </div>
      </SidebarHeader>

      <SidebarContent className="bg-[#070C14] pt-2">
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              {data.map((item) => {
                const IconComponent = item.icon;
                return (
                  <SidebarMenuItem key={item.title}>
                    <SidebarMenuButton
                      render={<a href={item.url} />}
                      className={`relative font-mono text-sm font-medium transition-colors hover:bg-white/5 hover:text-slate-100 ${
                        item.active
                          ? "bg-cyan-400/10 text-cyan-300 before:absolute before:inset-y-1.5 before:left-0 before:w-0.5 before:rounded-full before:bg-cyan-400"
                          : "text-slate-500"
                      }`}
                    >
                      <IconComponent /> {item.title}
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                );
              })}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter className="border-t border-white/10 bg-[#070C14] p-4">
        <div className="flex items-center gap-2 font-mono text-xs text-slate-500">
          <span className="telemetry-dot h-1.5 w-1.5 rounded-full bg-emerald-400" />
          Systems nominal
        </div>
      </SidebarFooter>
    </Sidebar>
  );
}
