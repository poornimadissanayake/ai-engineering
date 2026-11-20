// The one file to edit. Everything on the site, and everything the digital twin
// knows, comes from here. The twin will not answer anything that is not in this file.
//
// Every value below is a PLACEHOLDER. Replace it with your own details.

export type Experience = {
  role: string;
  company: string;
  period: string;
  summary: string;
  highlights: string[];
};

export type Project = {
  name: string;
  description: string;
  tech: string[];
  link?: string;
};

export type Profile = {
  name: string;
  role: string;
  location: string;
  tagline: string;
  about: string[];
  skills: string[];
  experience: Experience[];
  projects: Project[];
  contact: {
    email?: string;
    github?: string;
    linkedin?: string;
    website?: string;
  };
  // Extra things the twin may talk about that do not need a section on the page:
  // interests, what you are looking for, how you like to work.
  twinNotes: string[];
};

export const profile: Profile = {
  name: "Your Name",
  role: "Software Engineer",
  location: "Your City, Your Country",
  tagline: "Software engineer based in Your City. I build reliable web apps and small AI tools.",
  about: [
    "PLACEHOLDER: a short paragraph about who you are and what you work on.",
    "PLACEHOLDER: a second paragraph about what you care about in your work, or what you are learning right now.",
  ],
  skills: ["TypeScript", "React", "Next.js", "Python", "SQL", "LLM APIs"],
  experience: [
    {
      role: "Software Engineer",
      company: "Example Company",
      period: "2023 – present",
      summary: "PLACEHOLDER: one line on the team and what it does.",
      highlights: [
        "PLACEHOLDER: something you shipped and the result.",
        "PLACEHOLDER: something you improved, with a number if you have one.",
      ],
    },
    {
      role: "Junior Developer",
      company: "Another Example Ltd",
      period: "2021 – 2023",
      summary: "PLACEHOLDER: one line on the role.",
      highlights: ["PLACEHOLDER: a highlight from this role."],
    },
  ],
  projects: [
    {
      name: "Sample Project One",
      description: "PLACEHOLDER: a portfolio tracker that sends a note when holdings drift from target weights.",
      tech: ["n8n", "Google Sheets", "OpenRouter"],
      link: "https://example.com",
    },
    {
      name: "Sample Project Two",
      description: "PLACEHOLDER: this website, with a chat panel that answers questions about me.",
      tech: ["Next.js", "TypeScript", "Tailwind CSS", "OpenRouter"],
    },
  ],
  contact: {
    email: "you@example.com",
    github: "https://github.com/your-handle",
    linkedin: "https://www.linkedin.com/in/your-handle",
  },
  twinNotes: [
    "PLACEHOLDER: what kind of work or roles you are open to.",
    "PLACEHOLDER: an interest outside work you are happy to talk about.",
  ],
};
