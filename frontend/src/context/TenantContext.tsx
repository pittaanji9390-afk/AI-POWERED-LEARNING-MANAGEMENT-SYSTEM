import React, { createContext, useContext, useState } from "react";

interface TenantContextType {
  tenantId: string | null;
  tenantName: string | null;
  setTenant: (id: string, name: string) => void;
}

const TenantContext = createContext<TenantContextType | undefined>(undefined);

export const TenantProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [tenantId, setTenantId] = useState<string | null>(null);
  const [tenantName, setTenantName] = useState<string | null>("Global Platform");

  const setTenant = (id: string, name: string) => {
    localStorage.setItem("tenant_id", id);
    setTenantId(id);
    setTenantName(name);
  };

  return (
    <TenantContext.Provider value={{ tenantId, tenantName, setTenant }}>
      {children}
    </TenantContext.Provider>
  );
};

export const useTenant = () => {
  const context = useContext(TenantContext);
  if (!context) throw new Error("useTenant must be used within a TenantProvider");
  return context;
};
