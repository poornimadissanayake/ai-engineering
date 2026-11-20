import Chat from "@/components/Chat";
import { profile } from "@/content/profile";

const NAV = [
  { href: "#about", label: "About" },
  { href: "#experience", label: "Experience" },
  { href: "#projects", label: "Projects" },
  { href: "#twin", label: "Ask my twin" },
  { href: "#contact", label: "Contact" },
];

function Section({ id, title, children }: { id: string; title: string; children: React.ReactNode }) {
  return (
    <section id={id} className="scroll-mt-20 py-12">
      <h2 className="mb-6 text-sm font-semibold uppercase tracking-widest text-zinc-500 dark:text-zinc-400">
        {title}
      </h2>
      {children}
    </section>
  );
}

export default function Home() {
  const contactLinks = [
    profile.contact.email && { label: "Email", href: `mailto:${profile.contact.email}` },
    profile.contact.github && { label: "GitHub", href: profile.contact.github },
    profile.contact.linkedin && { label: "LinkedIn", href: profile.contact.linkedin },
    profile.contact.website && { label: "Website", href: profile.contact.website },
  ].filter((link): link is { label: string; href: string } => Boolean(link));

  return (
    <>
      <header className="sticky top-0 z-10 border-b border-zinc-200 bg-zinc-50/80 backdrop-blur dark:border-zinc-800 dark:bg-zinc-950/80">
        <nav className="mx-auto flex max-w-3xl items-center justify-between gap-4 px-6 py-4">
          <a href="#" className="font-semibold">
            {profile.name}
          </a>
          <ul className="hidden gap-5 text-sm text-zinc-600 sm:flex dark:text-zinc-400">
            {NAV.map((item) => (
              <li key={item.href}>
                <a href={item.href} className="hover:text-zinc-900 dark:hover:text-zinc-100">
                  {item.label}
                </a>
              </li>
            ))}
          </ul>
        </nav>
      </header>

      <main className="mx-auto max-w-3xl px-6">
        <section className="py-20">
          <p className="text-sm text-zinc-500 dark:text-zinc-400">{profile.location}</p>
          <h1 className="mt-2 text-4xl font-bold tracking-tight sm:text-5xl">{profile.name}</h1>
          <p className="mt-2 text-xl text-zinc-600 dark:text-zinc-300">{profile.role}</p>
          <p className="mt-6 max-w-xl text-lg leading-relaxed text-zinc-700 dark:text-zinc-300">
            {profile.tagline}
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <a
              href="#twin"
              className="rounded-lg bg-zinc-900 px-5 py-2.5 text-sm font-medium text-white hover:bg-zinc-700 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-300"
            >
              Talk to my digital twin
            </a>
            <a
              href="#contact"
              className="rounded-lg border border-zinc-300 px-5 py-2.5 text-sm font-medium hover:bg-zinc-100 dark:border-zinc-700 dark:hover:bg-zinc-900"
            >
              Get in touch
            </a>
          </div>
        </section>

        <Section id="about" title="About">
          <div className="space-y-4 leading-relaxed text-zinc-700 dark:text-zinc-300">
            {profile.about.map((paragraph, i) => (
              <p key={i}>{paragraph}</p>
            ))}
          </div>
          <ul className="mt-6 flex flex-wrap gap-2">
            {profile.skills.map((skill) => (
              <li
                key={skill}
                className="rounded-full bg-zinc-200 px-3 py-1 text-xs font-medium text-zinc-700 dark:bg-zinc-800 dark:text-zinc-300"
              >
                {skill}
              </li>
            ))}
          </ul>
        </Section>

        <Section id="experience" title="Experience">
          <ol className="space-y-8">
            {profile.experience.map((job) => (
              <li key={`${job.company}-${job.period}`}>
                <div className="flex flex-wrap items-baseline justify-between gap-2">
                  <h3 className="font-semibold">
                    {job.role} · <span className="text-zinc-600 dark:text-zinc-400">{job.company}</span>
                  </h3>
                  <span className="text-sm text-zinc-500">{job.period}</span>
                </div>
                <p className="mt-2 text-zinc-700 dark:text-zinc-300">{job.summary}</p>
                {job.highlights.length > 0 && (
                  <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-zinc-600 dark:text-zinc-400">
                    {job.highlights.map((h) => (
                      <li key={h}>{h}</li>
                    ))}
                  </ul>
                )}
              </li>
            ))}
          </ol>
        </Section>

        <Section id="projects" title="Projects">
          <div className="grid gap-4 sm:grid-cols-2">
            {profile.projects.map((project) => (
              <article
                key={project.name}
                className="rounded-xl border border-zinc-200 bg-white p-5 dark:border-zinc-800 dark:bg-zinc-900"
              >
                <h3 className="font-semibold">
                  {project.link ? (
                    <a href={project.link} className="hover:underline" target="_blank" rel="noreferrer">
                      {project.name} ↗
                    </a>
                  ) : (
                    project.name
                  )}
                </h3>
                <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">{project.description}</p>
                <p className="mt-3 text-xs text-zinc-500">{project.tech.join(" · ")}</p>
              </article>
            ))}
          </div>
        </Section>

        <Section id="twin" title="Talk to my digital twin">
          <Chat name={profile.name} />
        </Section>

        <Section id="contact" title="Contact">
          <ul className="flex flex-wrap gap-3">
            {contactLinks.map((link) => (
              <li key={link.label}>
                <a
                  href={link.href}
                  className="inline-block rounded-lg border border-zinc-300 px-4 py-2 text-sm hover:bg-zinc-100 dark:border-zinc-700 dark:hover:bg-zinc-900"
                  {...(link.href.startsWith("http") ? { target: "_blank", rel: "noreferrer" } : {})}
                >
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
        </Section>
      </main>

      <footer className="mx-auto max-w-3xl px-6 py-10 text-sm text-zinc-500">
        © {new Date().getFullYear()} {profile.name}
      </footer>
    </>
  );
}
