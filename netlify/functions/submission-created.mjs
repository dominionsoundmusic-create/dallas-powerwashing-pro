// Texts Maurice about every verified Netlify Forms submission on this site.
//
// Netlify runs this automatically after a form submission passes its spam filter
// (the "submission-created" event). It tidies the fields into one simple shape and posts
// them to the GoHighLevel workflow "Website Form - Text Maurice", which saves the lead as
// a contact and sends the text from the A2P-approved number.
//
// The same file is used on every Dominion site with forms. The workflow address lives in
// the FORM_TEXT_WEBHOOK environment variable in Netlify, not in the repo. If it is missing
// or GoHighLevel is down, the form still saves and the usual email still goes out; this
// function never blocks a submission.

const BRANDS = {
  "dominionwebdesignpro.com": "Dominion Web Design Pro",
  "houstonexpertroofers.com": "Houston Expert Roofers",
  "dfwexpertroofers.com": "DFW Expert Roofers",
  "houstonairandheating.com": "Houston Air & Heating",
  "dallasairandheating.com": "Dallas Air & Heating",
  "austinacservice.com": "Austin AC Service",
  "houstonpowerwashingpro.com": "Houston Power Washing Pro",
  "dallaspowerwashingpro.com": "Dallas Metro Power Washing Pro",
  "phoenixpoolcleaningpro.com": "Phoenix Pool Cleaning Pro",
  "tucsonpoolcleaningpro.com": "Tucson Pool Cleaning Pro",
  "yumapoolcleaningpro.com": "Yuma Pool Cleaning Pro",
  "dominionpoolpros.com": "Dominion Pool Pros",
};

const FORM_LABELS = {
  "homepage-contact": "Contact form",
  "site-check": "Free Site Check",
  "client-intake": "Client intake form",
  "free-ac-guide": "Free AC guide download",
  "austin-free-ac-guide": "Free AC guide download",
  "houston-hail-checklist": "Hail checklist download",
  "dallas-hail-checklist": "Hail checklist download",
};

const pick = (data, keys) => {
  for (const k of keys) {
    const v = data[k];
    if (typeof v === "string" && v.trim()) return v.trim();
  }
  return "";
};

const toE164 = (raw) => {
  const digits = (raw || "").replace(/\D/g, "");
  if (digits.length === 10) return "+1" + digits;
  if (digits.length === 11 && digits.startsWith("1")) return "+" + digits;
  return raw || "";
};

export function buildLead(payload) {
  const data = payload.data || {};
  const formName = payload.form_name || data["form-name"] || "form";
  const label = FORM_LABELS[formName] || (/contact|inquiry|quote/.test(formName) ? "Quote request" : formName);

  let host = "";
  try { host = new URL(payload.site_url || data.referrer || "").hostname.replace(/^www\./, ""); } catch {}
  const brand = BRANDS[host] || host || "your website";

  const name = pick(data, ["name", "Your name"]) || pick(data, ["business", "Business name"]);
  const [first, ...rest] = name.split(/\s+/);
  const phone = toE164(pick(data, ["phone", "Your phone", "Lead text phone", "Public phone"]));
  const email = pick(data, ["email", "Your email", "Lead email"]);

  const need = pick(data, ["need", "service", "situation"]);
  const where = pick(data, ["city", "location", "zip"]);
  let note = pick(data, ["message", "Anything else", "Your story"]);
  if (formName === "site-check") {
    const site = pick(data, ["website"]);
    const grade = pick(data, ["grade"]);
    note = [site && `Checked ${site}`, grade && `grade ${grade}`].filter(Boolean).join(", ") || note;
  }
  if (formName === "client-intake") {
    const pkg = pick(data, ["Package"]);
    const biz = pick(data, ["Business name"]);
    note = [biz, pkg && `package ${pkg}`].filter(Boolean).join(", ") || note;
  }
  const needs = [need, where && `in ${where}`].filter(Boolean).join(" ");
  let message = [needs, note].filter(Boolean).join(". ");
  if (message.length > 300) message = message.slice(0, 297) + "...";

  return {
    brand,
    form: label,
    site: host,
    summary: `${label} from ${brand}` + (need ? `. Needs: ${need}` : ""),
    name: name || "(no name given)",
    first_name: first || "",
    last_name: rest.join(" "),
    phone: phone || "",
    email: email || "",
    business: pick(data, ["business", "Business name"]),
    need,
    city: where,
    message: message || "(no message)",
  };
}

export const handler = async (event) => {
  try {
    const { payload } = JSON.parse(event.body || "{}");
    const url = process.env.FORM_TEXT_WEBHOOK;
    if (!payload || !url) return { statusCode: 200, body: "skipped" };
    const lead = buildLead(payload);
    const res = await fetch(url, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(lead),
    });
    console.log(`form-text: ${lead.summary} -> GoHighLevel ${res.status}`);
  } catch (err) {
    console.log("form-text failed:", err && err.message);
  }
  return { statusCode: 200, body: "ok" };
};
