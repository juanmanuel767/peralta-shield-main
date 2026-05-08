import { createFileRoute } from "@tanstack/react-router";
import { Layout } from "@/components/peralta/Layout";
import { Hero } from "@/components/peralta/Hero";
import { Stats } from "@/components/peralta/Stats";
import { FeatureGrid } from "@/components/peralta/FeatureGrid";
import { HowItWorks } from "@/components/peralta/HowItWorks";
import { Testimonials } from "@/components/peralta/Testimonials";
import { CTA } from "@/components/peralta/CTA";
import { MilitaryGrade } from "@/components/peralta/MilitaryGrade";

export const Route = createFileRoute("/")({
  component: Index,
});

function Index() {
  return (
    <Layout>
      <Hero />
      <Stats />
      <FeatureGrid />
      <MilitaryGrade />
      <HowItWorks />
      <Testimonials />
      <CTA />
    </Layout>
  );
}
