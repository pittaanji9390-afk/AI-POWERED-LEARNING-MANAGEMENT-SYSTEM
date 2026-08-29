import React, { useState } from "react";
import { Card } from "../../components/ui/card";
import { Badge } from "../../components/ui/badge";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Check, Sparkles, Shield, Tag, CreditCard, Lock, ArrowRight } from "lucide-react";

export const PricingPlansPage: React.FC = () => {
  const [isAnnual, setIsAnnual] = useState(true);
  const [selectedPlan, setSelectedPlan] = useState<string | null>(null);
  const [couponCode, setCouponCode] = useState("");
  const [appliedDiscount, setAppliedDiscount] = useState<number | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isPaid, setIsPaid] = useState(false);

  const plans = [
    {
      id: "free",
      name: "Starter Learner",
      monthlyPrice: 0,
      annualPrice: 0,
      description: "Ideal for individual self-paced learners exploring free public courses.",
      features: [
        "Access to all free public courses",
        "Community discussion board access",
        "Standard course completion badges",
        "5 AI tutor queries per day",
      ],
      popular: false,
    },
    {
      id: "pro",
      name: "Pro Engineer",
      monthlyPrice: 29,
      annualPrice: 24,
      description: "Complete career mastery with unlimited AI tutoring and verified certificates.",
      features: [
        "Unlimited access to 500+ premium courses",
        "Unlimited Socratic AI Tutor & code mentor",
        "Verifiable cryptographic certificates",
        "AI-generated personalized quizzes & labs",
        "Offline document & video downloads",
      ],
      popular: true,
    },
    {
      id: "enterprise",
      name: "Enterprise Organization",
      monthlyPrice: 99,
      annualPrice: 79,
      description: "Dedicated tenant isolation, team analytics, and custom AI course ingestion.",
      features: [
        "Dedicated multi-tenant workspace with custom branding",
        "Custom private course builder & AI curriculum generator",
        "Team skill analytics & mastery dashboards",
        "Single Sign-On (SSO / SAML / OIDC)",
        "99.99% SLA & Dedicated Support Manager",
      ],
      popular: false,
    },
  ];

  const handleApplyCoupon = (e: React.FormEvent) => {
    e.preventDefault();
    if (couponCode.toUpperCase() === "SAVE20" || couponCode.toUpperCase() === "LEARN2026") {
      setAppliedDiscount(20);
    } else {
      alert("Invalid coupon code. Try 'SAVE20' for 20% off.");
    }
  };

  const handleCheckout = () => {
    setIsProcessing(true);
    setTimeout(() => {
      setIsProcessing(false);
      setIsPaid(true);
    }, 1200);
  };

  const activePlanObj = plans.find((p) => p.id === selectedPlan);
  const rawPrice = activePlanObj ? (isAnnual ? activePlanObj.annualPrice : activePlanObj.monthlyPrice) : 0;
  const finalPrice = appliedDiscount ? rawPrice * (1 - appliedDiscount / 100) : rawPrice;

  return (
    <div className="max-w-6xl mx-auto space-y-12 py-4">
      {/* Header */}
      <div className="text-center space-y-4 max-w-2xl mx-auto">
        <Badge variant="primary">Predictable SaaS Pricing</Badge>
        <h1 className="text-3xl font-extrabold text-white sm:text-4xl">
          Accelerate your team with AI-grounded learning
        </h1>
        <p className="text-sm text-slate-400">
          Transparent subscription tiers with zero lock-in and instant team provisioning.
        </p>

        {/* Monthly / Annual Toggle */}
        <div className="flex items-center justify-center gap-3 pt-2">
          <span className={`text-xs font-medium ${!isAnnual ? "text-white" : "text-slate-400"}`}>Monthly Billing</span>
          <button
            onClick={() => setIsAnnual(!isAnnual)}
            className="w-12 h-6 bg-indigo-600 rounded-full p-1 transition-colors relative"
          >
            <div className={`h-4 w-4 rounded-full bg-white transition-transform ${isAnnual ? "translate-x-6" : "translate-x-0"}`} />
          </button>
          <span className={`text-xs font-medium flex items-center gap-1.5 ${isAnnual ? "text-white" : "text-slate-400"}`}>
            <span>Annual Billing</span>
            <Badge variant="success" className="text-[10px] px-1.5 py-0">Save 20%</Badge>
          </span>
        </div>
      </div>

      {/* Pricing Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {plans.map((plan) => {
          const price = isAnnual ? plan.annualPrice : plan.monthlyPrice;
          return (
            <Card
              key={plan.id}
              className={`p-6 flex flex-col justify-between relative transition-all ${
                plan.popular
                  ? "border-indigo-500 bg-slate-900/90 shadow-xl ring-1 ring-indigo-500/50"
                  : "border-slate-800 bg-slate-950/60"
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                  <Badge variant="primary" className="bg-indigo-600 text-white font-semibold">
                    Most Popular
                  </Badge>
                </div>
              )}

              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-bold text-white">{plan.name}</h3>
                  <p className="text-xs text-slate-400 mt-1 min-h-[32px]">{plan.description}</p>
                </div>

                <div className="flex items-baseline gap-1">
                  <span className="text-3xl font-extrabold text-white">${price}</span>
                  <span className="text-xs text-slate-400">/ user / month</span>
                </div>

                <div className="space-y-3 pt-4 border-t border-slate-800 text-xs">
                  {plan.features.map((feat, idx) => (
                    <div key={idx} className="flex items-start gap-2.5 text-slate-300">
                      <Check className="h-4 w-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                      <span>{feat}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="pt-8">
                <Button
                  variant={plan.popular ? "primary" : "secondary"}
                  className="w-full"
                  onClick={() => setSelectedPlan(plan.id)}
                >
                  {plan.id === "free" ? "Get Started Free" : `Upgrade to ${plan.name}`}
                </Button>
              </div>
            </Card>
          );
        })}
      </div>

      {/* Checkout Modal */}
      {selectedPlan && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <Card className="max-w-md w-full p-6 border-slate-700 bg-slate-900 shadow-2xl space-y-6">
            {!isPaid ? (
              <>
                <div className="flex items-center justify-between border-b border-slate-800 pb-4">
                  <div className="flex items-center gap-2">
                    <div className="p-2 bg-indigo-500/10 text-indigo-400 rounded-lg">
                      <CreditCard className="h-5 w-5" />
                    </div>
                    <div>
                      <h3 className="font-bold text-white text-base">Secure SaaS Checkout</h3>
                      <p className="text-xs text-slate-400">{activePlanObj?.name} ({isAnnual ? "Annual" : "Monthly"})</p>
                    </div>
                  </div>
                  <button onClick={() => setSelectedPlan(null)} className="text-slate-400 hover:text-white text-xs">✕</button>
                </div>

                {/* Coupon Input */}
                <form onSubmit={handleApplyCoupon} className="space-y-2">
                  <label className="text-xs text-slate-400 font-medium flex items-center gap-1">
                    <Tag className="h-3.5 w-3.5 text-indigo-400" /> Have a Promo Coupon?
                  </label>
                  <div className="flex gap-2">
                    <Input
                      placeholder="e.g. SAVE20"
                      value={couponCode}
                      onChange={(e) => setCouponCode(e.target.value)}
                    />
                    <Button type="submit" variant="secondary" size="sm">Apply</Button>
                  </div>
                  {appliedDiscount && (
                    <p className="text-xs text-emerald-400 font-medium">✓ Coupon applied: {appliedDiscount}% discount</p>
                  )}
                </form>

                {/* Order Summary */}
                <div className="p-4 bg-slate-950/80 rounded-xl border border-slate-800 text-xs space-y-2">
                  <div className="flex justify-between text-slate-400">
                    <span>Base Tier Price:</span>
                    <span>${rawPrice.toFixed(2)}/mo</span>
                  </div>
                  {appliedDiscount && (
                    <div className="flex justify-between text-emerald-400">
                      <span>Discount ({appliedDiscount}%):</span>
                      <span>-${(rawPrice * (appliedDiscount / 100)).toFixed(2)}/mo</span>
                    </div>
                  )}
                  <div className="flex justify-between font-bold text-white pt-2 border-t border-slate-800 text-sm">
                    <span>Total Due Today:</span>
                    <span>${finalPrice.toFixed(2)}/mo</span>
                  </div>
                </div>

                <div className="space-y-3">
                  <Button variant="primary" className="w-full flex items-center justify-center gap-2" isLoading={isProcessing} onClick={handleCheckout}>
                    <Lock className="h-4 w-4" />
                    <span>Authorize Payment & Activate</span>
                  </Button>
                  <p className="text-[10px] text-slate-500 text-center flex items-center justify-center gap-1">
                    <Shield className="h-3 w-3" /> End-to-end 256-bit encrypted tokenized payment.
                  </p>
                </div>
              </>
            ) : (
              <div className="text-center space-y-4 py-4">
                <div className="h-14 w-14 bg-emerald-500/10 text-emerald-400 rounded-full flex items-center justify-center mx-auto">
                  <Check className="h-7 w-7" />
                </div>
                <h3 className="text-xl font-bold text-white">Subscription Active!</h3>
                <p className="text-xs text-slate-400">
                  Your enterprise entitlements have been unlocked immediately.
                </p>
                <Button variant="primary" className="w-full" onClick={() => { setSelectedPlan(null); setIsPaid(false); }}>
                  Return to Dashboard
                </Button>
              </div>
            )}
          </Card>
        </div>
      )}
    </div>
  );
};
