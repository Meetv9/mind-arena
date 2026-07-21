# -*- coding: utf-8 -*-
"""
content.py — The full content library for MIND ARENA (ESG edition).

Everything the game draws from lives here, and it is now focused entirely on
ESG, sustainability, carbon markets, Life Cycle Assessment (LCA), carbon
accounting, SBTi and net zero, disclosure frameworks and climate regulation:

  * ESG speaking prompts / topics / props (emoji visual props)
  * A large, fact-checked ESG brain-teaser / quiz bank
  * Progressive ESG "boss" challenge generators
  * A speaking-coach teaching section (delivery technique — topic-neutral)
  * A descriptive ESG LEARNING library that teaches every topic in the quiz

Nothing here needs the internet. It is pure data + a few random generators so
the game always works offline.

FACT-CHECK NOTE: quiz answers and learning content were written to be accurate
as of 2023–2024. Global Warming Potential (GWP) values follow IPCC AR5 (100-year
basis) unless a different horizon is stated, and are given as rounded, clearly
qualified figures on purpose.
"""

import random
import string

# ---------------------------------------------------------------------------
# 1) ESG SPEAKING PROMPTS
#    Each item is (emoji_prop, prompt_text). The emoji is the "prop" the user
#    must weave into a persuasive / explanatory mini-speech about ESG.
# ---------------------------------------------------------------------------

SPEECH_PROMPTS = [
    ("🌍", "You have sixty seconds to convince a room of CEOs that ESG is a business strategy, not a cost."),
    ("🏭", "Explain Scope 1, 2, and 3 emissions to a factory owner who has never heard the terms."),
    ("♻️", "Pitch the circular economy to a company that still thinks 'take, make, dispose'."),
    ("🌱", "Persuade a sceptical board to commit to a science-based net-zero target."),
    ("💨", "Describe what a tonne of carbon dioxide actually is to someone who cannot picture it."),
    ("⚖️", "Argue that the 'S' in ESG matters just as much as the 'E'."),
    ("📉", "Convince investors that climate risk is financial risk."),
    ("🌡️", "Explain why 1.5°C of warming matters, using no scientific jargon."),
    ("🔋", "Make the case for a company to switch to 100% renewable electricity."),
    ("🌳", "Defend nature-based carbon removal — and be honest about its limits."),
    ("🧾", "Explain a carbon credit to a small-business owner in plain language."),
    ("🏦", "Persuade a bank to measure and cut its financed emissions."),
    ("🚗", "Pitch a plan to decarbonise a delivery fleet in under a minute."),
    ("🥩", "Talk about the climate footprint of food without lecturing or shaming anyone."),
    ("🌊", "Describe how a coastal community experiences climate change first-hand."),
    ("💧", "Argue that water stewardship belongs at the centre of every ESG strategy."),
    ("🏗️", "Explain 'embodied carbon' in buildings to a property developer."),
    ("📜", "Make the EU's carbon border tax (CBAM) sound simple and fair."),
    ("🤝", "Persuade a supplier to share its emissions data with you."),
    ("🎯", "Explain why 'net zero by 2050' is a target, not a slogan."),
    ("🔍", "Warn a marketing team about greenwashing — and how to avoid it."),
    ("🌐", "Speak for the Global South in a debate about who should pay for climate action."),
    ("🌾", "Give a voice to a smallholder farmer in a conversation about carbon markets."),
    ("⚡", "Argue that energy efficiency is the cheapest climate solution we ignore."),
    ("🗑️", "Reframe 'waste' as a resource in a two-minute pitch."),
    ("🐝", "Make the business case for protecting biodiversity, not just carbon."),
    ("🏛️", "Explain double materiality to a manager who finds it confusing."),
    ("📊", "Convince a CFO that measuring emissions is the first step to cutting them."),
    ("🌬️", "Sell the idea of a wind farm to a community that fears change."),
    ("🔥", "Explain 'carbon leakage' and why border carbon rules exist."),
    ("🧭", "Argue that a 'just transition' is what makes climate action possible."),
    ("💰", "Explain the difference between a carbon tax and cap-and-trade to a student."),
    ("🌞", "Give a hopeful two-minute vision of a fully decarbonised city in 2050."),
    ("📦", "Explain a product's life cycle 'from cradle to grave' using one everyday object."),
    ("🧪", "Describe what a Life Cycle Assessment reveals that a price tag never shows."),
    ("🏅", "Argue that ESG ratings help investors — and where they fall short."),
    ("🌍", "You are a Chief Sustainability Officer. Give your opening speech on day one."),
    ("🚭", "Convince a heavy-emitting company that transition beats denial."),
    ("🌲", "Defend the idea that the cheapest carbon we can cut is the carbon we never emit."),
    ("📈", "Explain why a company should set both near-term and long-term climate targets."),
    ("🧊", "Describe the melting Arctic to someone who has never felt real cold."),
    ("🤖", "Argue whether AI and data centres are a climate problem or a climate solution."),
    ("🛠️", "Pitch retrofitting old buildings as a climate megaproject."),
    ("🍽️", "Give a two-minute plan to cut food waste across a supply chain."),
    ("👥", "Make the case that good governance is what makes 'E' and 'S' credible."),
    ("🌏", "Explain the Paris Agreement's core promise in words a child would understand."),
    ("💎", "Argue that transparency, not perfection, is what builds ESG trust."),
    ("🔗", "Explain why Scope 3 — the value chain — is usually the hardest and biggest challenge."),
    ("🌡️", "Persuade a town that adapting to climate change is as urgent as preventing it."),
    ("🪫", "Argue that offsets should be the last resort, not the first move."),
    ("🏆", "Celebrate a company that hit a hard climate target — and explain how they did it."),
    ("🌿", "Explain why 'nature-positive' is becoming the next word after 'net zero'."),
    ("⛏️", "Discuss the human cost and promise of mining the metals a green economy needs."),
    ("🚿", "Make the case for the circular economy using a single household habit."),
    ("📻", "You have one radio minute to explain why COP climate summits matter."),
    ("🧯", "Explain climate adaptation using a community that survived a flood or heatwave."),
    ("🕊️", "Give a short, powerful speech on climate justice between rich and poor nations."),
    ("🌱", "Convince a start-up founder to build sustainability in from day one."),
    ("🔬", "Explain how emission factors turn 'litres of fuel' into 'tonnes of CO2'."),
    ("🌍", "You are addressing the whole human race for sixty seconds on our shared climate future. Go."),

    # ===== EXPANSION BANK (more speaking variety so prompts don't feel repetitive) =====
    ("🏷️", "Explain the difference between ESG and CSR to someone who thinks they're the same thing."),
    ("📗", "In one minute, explain what the GHG Protocol is and why almost everyone uses it."),
    ("🧮", "Teach a friend how to calculate their household's rough annual carbon footprint."),
    ("🔗", "Explain Scope 1, 2 and 3 emissions using a single loaf of bread's journey."),
    ("🌾", "Convince a farmer that regenerative agriculture is both good soil and good business."),
    ("💧", "Give a persuasive talk on why water stewardship matters as much as carbon."),
    ("🏭", "Explain to a factory manager what a Life Cycle Assessment would reveal about their product."),
    ("📉", "Describe what 'science-based targets' means and why 'net zero someday' isn't enough."),
    ("🧾", "Explain carbon accounting to a small-business owner in plain, friendly language."),
    ("⚖️", "Make the case that strong governance is the 'G' that makes the 'E' and 'S' actually happen."),
    ("🌡️", "Explain why the 1.5°C threshold matters, and what happens if we blow past it."),
    ("🪙", "Explain how a carbon market puts a price on pollution, to a curious teenager."),
    ("🌲", "Argue for or against carbon offsets as a tool for reaching net zero."),
    ("🔋", "Pitch why energy efficiency is the cheapest 'clean energy' we already have."),
    ("♻️", "Explain the circular economy to someone who just wants to know why recycling isn't enough."),
    ("📊", "Explain what 'materiality' means in sustainability reporting, using a simple example."),
    ("🚢", "Describe how global shipping and supply chains hide a huge chunk of Scope 3 emissions."),
    ("🏦", "Convince a bank that climate risk is financial risk, not charity."),
    ("🌀", "Explain 'greenwashing' and give three warning signs to watch for."),
    ("🛰️", "Explain how satellites and sensors are changing how we measure real emissions."),
    ("🧑‍🤝‍🧑", "Give a short speech on why a 'just transition' must protect workers, not just the planet."),
    ("🏙️", "Explain how cities can cut emissions faster than countries, with one concrete example."),
    ("🐝", "Make the case that biodiversity loss is as urgent as climate change."),
    ("🍽️", "Explain how food choices connect to methane, land use and emissions."),
    ("🔥", "Explain what 'stranded assets' are and why investors suddenly care."),
    ("📜", "Explain the Paris Agreement's core promise in language a ten-year-old would get."),
    ("🧭", "Explain the difference between carbon neutral, net zero and climate positive."),
    ("💡", "Pitch one everyday habit that cuts emissions more than people expect, and prove it."),
    ("🌊", "Explain why oceans are our biggest carbon sink and why that's fragile."),
    ("🏗️", "Explain 'embodied carbon' in buildings and why concrete and steel are the problem."),
    ("🚗", "Argue whether electric vehicles are truly clean once you count the whole life cycle."),
    ("📈", "Explain why disclosing emissions is the first step no company can skip."),
    ("🧊", "Describe the feedback loops that make Arctic melting a self-accelerating problem."),
    ("🤝", "Explain how stakeholder capitalism differs from shareholder-only thinking."),
    ("🌻", "Convince a sceptic that sustainability and profit are not enemies."),
    ("🧯", "Explain climate mitigation vs adaptation, and why we need both at once."),
    ("🪫", "Explain why the grid — not just the car — decides how clean an EV really is."),
    ("📕", "Explain what a materiality assessment is and how a company picks what to report."),
    ("🌐", "Explain 'double materiality' and why European regulators insist on it."),
    ("🧪", "Explain what an emission factor is, using electricity as your example."),
    ("🏔️", "Give a vivid one-minute talk on what a warmer world means for the Himalayas."),
    ("🛢️", "Explain why fossil-fuel subsidies undercut every climate policy we pass."),
    ("🌪️", "Connect extreme weather events to climate change without overstating the science."),
    ("🧵", "Explain the environmental cost hidden inside fast fashion."),
    ("🔎", "Explain what 'assurance' means for sustainability data and why it builds trust."),
    ("🗳️", "Give a speech on why climate action needs policy, not just personal choices."),
    ("🏝️", "Speak for a small island nation on why climate change is an existential threat."),
    ("🌉", "Explain how green bonds channel money toward climate-friendly projects."),
    ("🧑‍🏭", "Explain 'Scope 3' to a supplier who thinks emissions are their customer's problem."),
    ("📅", "Explain why a baseline year matters when a company sets emission targets."),
    ("🕰️", "Explain the carbon budget concept: why timing, not just totals, decides everything."),
    ("🌿", "Explain 'nature-based solutions' and one place they genuinely work."),
    ("💰", "Explain 'internal carbon pricing' and why smart companies charge themselves for CO2."),
    ("🚌", "Pitch public transport as one of the highest-impact climate tools cities have."),
    ("🧑‍⚖️", "Explain 'climate litigation' and why courtrooms are becoming climate battlegrounds."),
    ("🔌", "Explain what 'electrification of everything' means for cutting emissions."),
    ("🏜️", "Explain desertification and how it links land degradation to livelihoods."),
    ("📦", "Explain how 'last-mile delivery' became a surprising emissions hotspot."),
    ("🧬", "Explain why measuring is the foundation — you can't manage what you don't measure."),
    ("🌤️", "Give a hopeful one-minute speech on a realistic clean-energy future."),
    ("🏅", "Explain what 'additionality' means for a carbon offset to actually count."),
    ("🗺️", "Explain why the Global South's development and climate goals must go together."),
    ("🪵", "Explain why not all 'renewable' biomass is automatically low-carbon."),
    ("🧑‍💼", "Convince a CEO that sustainability belongs in the boardroom, not a side team."),
    ("🌎", "Explain 'common but differentiated responsibilities' and why fairness is core to climate deals."),
]

# ---------------------------------------------------------------------------
# 2) ESG BRAIN TEASERS / QUIZ  (fact-checked)
#    Each: {"type": category, "q": question, "a": answer}
# ---------------------------------------------------------------------------

BRAIN_TEASERS = [
    # ---- ESG Basics ----
    {"type": "ESG Basics", "q": "What do the three letters in 'ESG' stand for?", "a": "Environmental, Social, and Governance."},
    {"type": "ESG Basics", "q": "In which 2004 UN-backed report did the term 'ESG' first become popular?", "a": "'Who Cares Wins' — a UN Global Compact report to the financial sector."},
    {"type": "ESG Basics", "q": "What is 'greenwashing'?", "a": "Making misleading or exaggerated claims that a product, service, or company is more environmentally friendly than it really is."},
    {"type": "ESG Basics", "q": "What is a 'materiality assessment' in ESG?", "a": "A process to identify which ESG issues matter most to a business and its stakeholders, so reporting and effort focus on them."},
    {"type": "ESG Basics", "q": "What does 'double materiality' mean?", "a": "Looking at both how sustainability issues affect the company financially AND how the company affects people and the planet (impact materiality)."},
    {"type": "ESG Basics", "q": "How many UN Sustainable Development Goals (SDGs) are there?", "a": "17."},
    {"type": "ESG Basics", "q": "What is a 'just transition'?", "a": "Moving to a low-carbon economy in a way that is fair to the workers and communities who depend on high-carbon industries."},
    {"type": "ESG Basics", "q": "What is the 'circular economy'?", "a": "An economic model that designs out waste by reusing, repairing, refurbishing, and recycling materials in loops — instead of 'take, make, dispose'."},
    {"type": "ESG Basics", "q": "What does 'PRI' stand for in responsible investing?", "a": "The Principles for Responsible Investment — a UN-supported investor initiative."},
    {"type": "ESG Basics", "q": "What is the difference between 'carbon neutral' and 'net zero'?", "a": "Carbon neutral usually means balancing emissions with offsets; net zero means deeply cutting all emissions across the value chain and neutralising only the small residual — a more rigorous, science-based goal."},

    # ---- GHG Protocol & Scopes ----
    {"type": "GHG Protocol", "q": "What are Scope 1 emissions?", "a": "Direct emissions from sources a company owns or controls — e.g. fuel burned in its boilers, furnaces, and vehicles."},
    {"type": "GHG Protocol", "q": "What are Scope 2 emissions?", "a": "Indirect emissions from the purchased energy a company uses — electricity, steam, heating, and cooling it buys."},
    {"type": "GHG Protocol", "q": "What are Scope 3 emissions?", "a": "All other indirect emissions in a company's value chain, both upstream and downstream — e.g. purchased goods, business travel, and use of sold products."},
    {"type": "GHG Protocol", "q": "How many categories does Scope 3 have under the GHG Protocol?", "a": "15 — eight upstream and seven downstream."},
    {"type": "GHG Protocol", "q": "For most companies, which scope is usually the largest?", "a": "Scope 3 (the value chain) — often the great majority of the total footprint."},
    {"type": "GHG Protocol", "q": "What are the two accounting methods for Scope 2 emissions?", "a": "Location-based (using the average grid emission factor) and market-based (reflecting the energy contracts a company buys, like renewables)."},
    {"type": "GHG Protocol", "q": "What does 'CO2e' (carbon dioxide equivalent) mean?", "a": "A common unit that converts every greenhouse gas into the amount of CO2 that would cause the same warming, using each gas's Global Warming Potential."},
    {"type": "GHG Protocol", "q": "What does GWP (Global Warming Potential) measure?", "a": "How much heat a greenhouse gas traps compared with CO2 over a set period — usually 100 years."},
    {"type": "GHG Protocol", "q": "Which standard defines Scopes 1, 2, and 3?", "a": "The GHG Protocol Corporate Standard, developed by WRI and WBCSD."},
    {"type": "GHG Protocol", "q": "Roughly how much more potent is methane (CH4) than CO2 over 100 years?", "a": "About 28 times (IPCC AR5) — and far higher, around 80 times, over a 20-year horizon."},
    {"type": "GHG Protocol", "q": "Which greenhouse gas has the highest GWP among the main Kyoto gases?", "a": "Sulphur hexafluoride (SF6) — over 20,000 times CO2 over 100 years."},
    {"type": "GHG Protocol", "q": "What is an 'emission factor'?", "a": "A value that converts an activity — like litres of fuel or kWh of electricity — into the greenhouse gases it produces."},
    {"type": "GHG Protocol", "q": "What is the simplest formula for estimating emissions?", "a": "Activity data × emission factor = emissions (e.g. litres of diesel × kgCO2e per litre)."},

    # ---- Carbon Markets ----
    {"type": "Carbon Markets", "q": "What is one carbon credit equal to?", "a": "One tonne of CO2 equivalent (CO2e) reduced, avoided, or removed from the atmosphere."},
    {"type": "Carbon Markets", "q": "What is the difference between compliance and voluntary carbon markets?", "a": "Compliance markets are created by law or regulation (like the EU ETS); voluntary markets let organisations buy credits by choice to meet their own climate goals."},
    {"type": "Carbon Markets", "q": "What is 'cap and trade'?", "a": "A system that sets a cap (limit) on total emissions and lets companies trade allowances; the cap falls over time to force reductions."},
    {"type": "Carbon Markets", "q": "What was the world's first major carbon market, launched in 2005?", "a": "The EU Emissions Trading System (EU ETS)."},
    {"type": "Carbon Markets", "q": "What is 'additionality' in carbon offsetting?", "a": "The requirement that the emission reduction would not have happened without the carbon-credit funding — proving the project is genuinely extra."},
    {"type": "Carbon Markets", "q": "Which article of the Paris Agreement governs international carbon markets?", "a": "Article 6."},
    {"type": "Carbon Markets", "q": "What does 'REDD+' broadly stand for?", "a": "Reducing Emissions from Deforestation and forest Degradation — plus conservation and sustainable forest management."},
    {"type": "Carbon Markets", "q": "Name two major voluntary carbon-credit standards.", "a": "Verra (the Verified Carbon Standard) and the Gold Standard."},
    {"type": "Carbon Markets", "q": "What is the difference between a carbon tax and cap-and-trade?", "a": "A carbon tax fixes the price of emitting; cap-and-trade fixes the quantity (the cap) and lets the market set the price."},
    {"type": "Carbon Markets", "q": "What is CORSIA?", "a": "The Carbon Offsetting and Reduction Scheme for International Aviation, run by ICAO to offset growth in airline emissions."},

    # ---- Life Cycle Assessment (LCA) ----
    {"type": "LCA", "q": "What does a Life Cycle Assessment (LCA) do?", "a": "Measures the environmental impacts of a product, service, or system across its whole life cycle — from raw materials to disposal."},
    {"type": "LCA", "q": "Which ISO standards govern LCA?", "a": "ISO 14040 and ISO 14044."},
    {"type": "LCA", "q": "What are the four phases of an LCA?", "a": "1) Goal & scope definition, 2) Inventory analysis (LCI), 3) Impact assessment (LCIA), 4) Interpretation."},
    {"type": "LCA", "q": "What does 'cradle to grave' mean in LCA?", "a": "Assessing impacts across the full life cycle — raw material extraction, production, use, and end-of-life disposal."},
    {"type": "LCA", "q": "What does 'cradle to gate' mean?", "a": "Assessing impacts from raw materials up to the point the product leaves the factory gate — not including its use or disposal."},
    {"type": "LCA", "q": "What is a 'functional unit' in an LCA?", "a": "The quantified reference all impacts are measured against (e.g. '1 litre of packaged milk delivered'), so products can be compared fairly."},
    {"type": "LCA", "q": "What is an EPD (Environmental Product Declaration)?", "a": "A verified, LCA-based document that transparently reports a product's environmental impacts (governed by ISO 14025)."},
    {"type": "LCA", "q": "What is 'embodied carbon'?", "a": "The greenhouse gases emitted in making a product or material — extraction, manufacturing, and transport — separate from emissions during its use."},

    # ---- Carbon Accounting ----
    {"type": "Carbon Accounting", "q": "What is a 'base year' in carbon accounting?", "a": "A reference year against which a company tracks and compares its emissions over time."},
    {"type": "Carbon Accounting", "q": "Name the three approaches for setting organisational boundaries.", "a": "Equity share, financial control, and operational control."},
    {"type": "Carbon Accounting", "q": "What does PCAF help measure?", "a": "Financed emissions — the greenhouse gases linked to banks' and investors' loans and investments (Partnership for Carbon Accounting Financials)."},
    {"type": "Carbon Accounting", "q": "What are 'financed emissions'?", "a": "The share of a borrower's or investee's emissions attributed to the financial institution funding them (Scope 3, category 15)."},

    # ---- SBTi & Net Zero ----
    {"type": "SBTi & Net Zero", "q": "What does 'SBTi' stand for?", "a": "The Science Based Targets initiative."},
    {"type": "SBTi & Net Zero", "q": "Which organisations founded the SBTi?", "a": "CDP, the UN Global Compact, WRI, and WWF."},
    {"type": "SBTi & Net Zero", "q": "Which temperature limit do science-based targets aim to align with?", "a": "Limiting warming to 1.5°C above pre-industrial levels."},
    {"type": "SBTi & Net Zero", "q": "Under the SBTi Net-Zero Standard, roughly how much must a company cut before neutralising the rest?", "a": "About 90% deep emission cuts, neutralising only the residual ~10%."},
    {"type": "SBTi & Net Zero", "q": "When must a company set a Scope 3 target under SBTi rules?", "a": "When Scope 3 is 40% or more of its total emissions."},
    {"type": "SBTi & Net Zero", "q": "What is the difference between a near-term and a long-term science-based target?", "a": "Near-term targets cover roughly the next 5–10 years; long-term targets set the path to net zero by no later than 2050."},

    # ---- Frameworks & Disclosure ----
    {"type": "Frameworks", "q": "What does 'GRI' stand for?", "a": "The Global Reporting Initiative — widely used standards focused on a company's impacts on the economy, environment, and people."},
    {"type": "Frameworks", "q": "What was the TCFD, and what are its four pillars?", "a": "The Task Force on Climate-related Financial Disclosures; its pillars are Governance, Strategy, Risk Management, and Metrics & Targets."},
    {"type": "Frameworks", "q": "What is the ISSB, and what did it publish in 2023?", "a": "The International Sustainability Standards Board (under the IFRS Foundation); it issued IFRS S1 (general sustainability) and IFRS S2 (climate) standards."},
    {"type": "Frameworks", "q": "What is the CSRD?", "a": "The EU's Corporate Sustainability Reporting Directive, which requires detailed sustainability reporting using the ESRS standards and double materiality."},
    {"type": "Frameworks", "q": "What does SASB focus on (now part of the ISSB)?", "a": "Industry-specific, financially material sustainability topics aimed at investors."},
    {"type": "Frameworks", "q": "What is India's BRSR?", "a": "The Business Responsibility and Sustainability Report, mandated by SEBI for the top 1,000 listed companies, based on the nine NGRBC principles."},
    {"type": "Frameworks", "q": "What does 'CDP' stand for as a disclosure system?", "a": "Formerly the 'Carbon Disclosure Project'; now simply CDP — a global environmental disclosure platform for companies, cities, and regions."},

    # ---- Regulation & Climate Science ----
    {"type": "Regulation", "q": "In what year was the Paris Agreement adopted, and at which COP?", "a": "2015, at COP21."},
    {"type": "Regulation", "q": "What is the main temperature goal of the Paris Agreement?", "a": "Hold warming to well below 2°C, and pursue efforts to limit it to 1.5°C above pre-industrial levels."},
    {"type": "Regulation", "q": "What does 'NDC' mean under the Paris Agreement?", "a": "Nationally Determined Contribution — each country's self-set climate pledge, strengthened over time."},
    {"type": "Regulation", "q": "What is the EU CBAM?", "a": "The Carbon Border Adjustment Mechanism — an EU carbon price on imports of certain carbon-intensive goods, to prevent 'carbon leakage'."},
    {"type": "Regulation", "q": "Name three sectors covered by the EU CBAM.", "a": "Any three of: cement, iron & steel, aluminium, fertilisers, electricity, and hydrogen."},
    {"type": "Regulation", "q": "By what year has India pledged to reach net zero?", "a": "2070 — announced at COP26 in Glasgow (2021)."},
    {"type": "Regulation", "q": "What global net-zero year is broadly consistent with limiting warming to 1.5°C?", "a": "Around 2050."},
    {"type": "Regulation", "q": "What does 'carbon leakage' mean?", "a": "When climate rules push production — and its emissions — to move to countries with weaker rules, instead of actually cutting global emissions."},
    {"type": "Climate Science", "q": "What does the 'greenhouse effect' describe?", "a": "Gases in the atmosphere trapping the sun's heat and warming the planet — intensified by human-made emissions."},
    {"type": "Regulation", "q": "What 1997 treaty first set binding emission-reduction targets for developed countries?", "a": "The Kyoto Protocol."},

    # ===== EXPANSION BANK (more variety so questions don't feel repetitive) =====
    # ---- ESG Basics & Investing ----
    {"type": "ESG Basics", "q": "Who counts as a company's 'stakeholders'?", "a": "Any group that affects or is affected by the company — employees, customers, suppliers, communities, investors, and regulators."},
    {"type": "ESG Basics", "q": "What is 'ESG integration' in investing?", "a": "Systematically factoring ESG risks and opportunities into financial analysis and investment decisions."},
    {"type": "ESG Basics", "q": "What is 'impact investing'?", "a": "Investing to create measurable positive social or environmental impact alongside a financial return."},
    {"type": "ESG Basics", "q": "What is a 'B Corp'?", "a": "A company certified by B Lab for meeting high, verified standards of social and environmental performance, accountability, and transparency."},
    {"type": "ESG Basics", "q": "How does CSR differ from ESG?", "a": "CSR (Corporate Social Responsibility) is a broader, often voluntary/philanthropic idea; ESG is the measurable, data-driven framework investors use to assess it."},
    {"type": "ESG Basics", "q": "What is 'stakeholder capitalism'?", "a": "The idea that companies should serve all stakeholders — workers, society, the environment — not shareholders alone."},
    {"type": "ESG Basics", "q": "What is the 'triple bottom line'?", "a": "Measuring success by three P's — People, Planet, and Profit — rather than profit alone."},
    {"type": "ESG Basics", "q": "What is 'natural capital'?", "a": "The world's stock of natural assets — soil, air, water, and living things — that provide value and services to people and the economy."},
    {"type": "ESG Basics", "q": "What are the three pillars of sustainable development?", "a": "Environmental, social, and economic — often summed up as 'planet, people, prosperity'."},
    {"type": "ESG Basics", "q": "How is 'fiduciary duty' connected to ESG?", "a": "It's a manager's legal duty to act in clients' best interests; ESG risks are increasingly treated as financially material to that duty."},

    # ---- Governance ----
    {"type": "Governance", "q": "Name two core governance topics in ESG.", "a": "Any two: board independence and diversity, executive pay, anti-corruption/bribery, business ethics, shareholder rights, and transparency."},
    {"type": "Governance", "q": "What does 'board independence' mean?", "a": "Having directors with no material ties to management, so they can objectively oversee the company on behalf of shareholders."},
    {"type": "Governance", "q": "What is 'say on pay'?", "a": "A shareholder vote on a company's executive-compensation policy."},
    {"type": "Governance", "q": "What is a 'whistleblower' policy?", "a": "A system that lets employees safely report misconduct without fear of retaliation."},

    # ---- Social ----
    {"type": "Social", "q": "What does 'DEI' stand for?", "a": "Diversity, Equity, and Inclusion."},
    {"type": "Social", "q": "What is a 'living wage'?", "a": "Pay high enough to cover a worker's basic needs — housing, food, healthcare — in their location, often above the legal minimum wage."},
    {"type": "Social", "q": "What is 'human rights due diligence'?", "a": "A process by which companies identify, prevent, and address human-rights harms across their operations and supply chains."},
    {"type": "Social", "q": "What is 'modern slavery' in an ESG context?", "a": "Forced labour, human trafficking, and exploitation that companies must find and remove from their supply chains."},
    {"type": "Social", "q": "What does a 'social licence to operate' mean?", "a": "The ongoing acceptance and trust granted to a company by local communities and stakeholders."},

    # ---- Climate Science ----
    {"type": "Climate Science", "q": "What is the difference between climate 'mitigation' and 'adaptation'?", "a": "Mitigation reduces or prevents emissions (tackling the cause); adaptation adjusts to climate impacts already happening (managing the effects)."},
    {"type": "Climate Science", "q": "What is a 'carbon sink'?", "a": "A reservoir that absorbs more carbon than it releases — for example forests, soils, and the oceans."},
    {"type": "Climate Science", "q": "Which period is the usual 'pre-industrial baseline' for warming targets?", "a": "Roughly 1850–1900, before large-scale fossil-fuel emissions."},
    {"type": "Climate Science", "q": "What is a climate 'tipping point'?", "a": "A threshold beyond which part of the climate system changes in a way that is hard to reverse — e.g. an ice-sheet collapse."},
    {"type": "Climate Science", "q": "Which gas is the single largest contributor to human-caused warming?", "a": "Carbon dioxide (CO2), mainly from burning fossil fuels."},
    {"type": "Climate Science", "q": "What is 'ocean acidification'?", "a": "The ocean turning more acidic as it absorbs CO2, which harms shellfish and coral reefs."},
    {"type": "Climate Science", "q": "What is a 'carbon budget'?", "a": "The total amount of CO2 the world can still emit while staying within a temperature limit such as 1.5°C."},
    {"type": "Climate Science", "q": "What is the IPCC?", "a": "The Intergovernmental Panel on Climate Change — the UN body that assesses and summarises climate science."},
    {"type": "Climate Science", "q": "What is 'carbon sequestration'?", "a": "Capturing and storing CO2 for the long term — whether by nature (trees, soil) or by technology."},
    {"type": "Climate Science", "q": "What does 'CCS' stand for?", "a": "Carbon Capture and Storage — trapping CO2 from industry or power plants and storing it underground."},
    {"type": "Climate Science", "q": "What is 'Direct Air Capture' (DAC)?", "a": "Technology that pulls CO2 directly out of the ambient air for storage or use."},

    # ---- GHG Protocol (deeper) ----
    {"type": "GHG Protocol", "q": "Give one example of an upstream Scope 3 category.", "a": "Any of: purchased goods & services, capital goods, fuel- and energy-related activities, upstream transport, waste, business travel, or employee commuting."},
    {"type": "GHG Protocol", "q": "Give one example of a downstream Scope 3 category.", "a": "Any of: downstream transport, processing of sold products, use of sold products, end-of-life of sold products, leased assets, franchises, or investments."},
    {"type": "GHG Protocol", "q": "How many greenhouse gases does the GHG Protocol cover, and name a few?", "a": "Seven: CO2, CH4, N2O, HFCs, PFCs, SF6, and NF3."},
    {"type": "GHG Protocol", "q": "Roughly how much more potent is nitrous oxide (N2O) than CO2 over 100 years?", "a": "About 265 times (IPCC AR5)."},
    {"type": "GHG Protocol", "q": "What is a 'GHG inventory'?", "a": "A complete account of an organisation's greenhouse-gas emissions across all relevant scopes."},
    {"type": "GHG Protocol", "q": "Over what time horizon is GWP usually expressed?", "a": "100 years — though a 20-year horizon is also used to highlight short-lived but potent gases like methane."},
    {"type": "GHG Protocol", "q": "What does a 'PPA' let a company do for its Scope 2?", "a": "A Power Purchase Agreement — a long-term contract to buy renewable electricity, used to lower market-based Scope 2 emissions."},
    {"type": "GHG Protocol", "q": "What is a REC (or Guarantee of Origin)?", "a": "A certificate proving one MWh of electricity came from renewables, used in market-based Scope 2 accounting."},

    # ---- Carbon Markets (deeper) ----
    {"type": "Carbon Markets", "q": "What is the difference between 'avoidance' and 'removal' carbon credits?", "a": "Avoidance credits prevent emissions that would otherwise occur (e.g. protecting a forest); removal credits take CO2 out of the atmosphere (e.g. reforestation or direct air capture)."},
    {"type": "Carbon Markets", "q": "What is 'double counting' in carbon markets?", "a": "When the same emission reduction is claimed by more than one party — a key risk that Paris Article 6 rules aim to prevent."},
    {"type": "Carbon Markets", "q": "What is a 'carbon allowance'?", "a": "A permit under a cap-and-trade system that lets the holder emit one tonne of CO2e."},
    {"type": "Carbon Markets", "q": "What does 'permanence' mean in carbon offsetting?", "a": "Whether the stored carbon truly stays locked away long-term — a forest, for instance, can burn and release it again."},
    {"type": "Carbon Markets", "q": "What is the 'social cost of carbon'?", "a": "An estimate, in money, of the damage caused by emitting one extra tonne of CO2."},
    {"type": "Carbon Markets", "q": "What does 'MRV' stand for in carbon projects?", "a": "Monitoring, Reporting, and Verification — how a credit's claimed reductions are proven real."},
    {"type": "Carbon Markets", "q": "What was the 'CDM' under the Kyoto Protocol?", "a": "The Clean Development Mechanism — it let developed countries earn credits by funding emission-cutting projects in developing countries."},
    {"type": "Carbon Markets", "q": "What is a credit's 'vintage'?", "a": "The year in which the emission reduction or removal that the credit represents actually happened."},
    {"type": "Carbon Markets", "q": "What is an 'internal carbon price'?", "a": "A price a company puts on its own emissions to steer investment and purchasing decisions toward lower-carbon options."},

    # ---- LCA (deeper) ----
    {"type": "LCA", "q": "What does 'cradle to cradle' mean?", "a": "A circular life-cycle approach where end-of-life materials become inputs for new products, aiming for zero waste."},
    {"type": "LCA", "q": "What are 'PCRs' in the context of EPDs?", "a": "Product Category Rules — the standard recipe that makes EPDs for similar products comparable."},
    {"type": "LCA", "q": "Name two impact categories an LCA might assess besides climate change.", "a": "Any two: water use, land use, acidification, eutrophication, human toxicity, resource depletion, or ozone depletion."},
    {"type": "LCA", "q": "What is a 'hotspot' in an LCA?", "a": "The life-cycle stage or process responsible for the largest share of a product's environmental impact."},
    {"type": "LCA", "q": "What does 'gate to gate' cover in LCA?", "a": "Only the impacts of the processes within a single facility or production step."},
    {"type": "LCA", "q": "What is the difference between 'attributional' and 'consequential' LCA?", "a": "Attributional describes a product's impacts as they are; consequential models how impacts change as a result of a decision."},

    # ---- SBTi & Targets (deeper) ----
    {"type": "SBTi & Net Zero", "q": "What is a corporate 'transition plan'?", "a": "A concrete roadmap of actions, investments, and milestones showing how a company will hit its climate targets."},
    {"type": "SBTi & Net Zero", "q": "What is carbon 'insetting' (versus offsetting)?", "a": "Cutting or removing emissions inside a company's own value chain, rather than buying external offsets."},
    {"type": "SBTi & Net Zero", "q": "What are 'residual emissions' in a net-zero plan?", "a": "The small share of emissions that can't yet be eliminated and must be neutralised with carbon removals."},
    {"type": "SBTi & Net Zero", "q": "What does 'abatement' mean?", "a": "Actually reducing emissions at the source — as opposed to offsetting them elsewhere."},
    {"type": "SBTi & Net Zero", "q": "What is the 'mitigation hierarchy' for climate action?", "a": "Avoid, then reduce, and only for the unavoidable remainder, remove or offset."},
    {"type": "SBTi & Net Zero", "q": "What does 'FLAG' refer to in SBTi guidance?", "a": "Forest, Land and Agriculture — target-setting guidance for land-intensive companies."},

    # ---- Frameworks & Regulation (deeper) ----
    {"type": "Frameworks", "q": "What are the 'ESRS'?", "a": "The European Sustainability Reporting Standards that companies use to report under the EU's CSRD."},
    {"type": "Frameworks", "q": "What is the 'SFDR'?", "a": "The EU's Sustainable Finance Disclosure Regulation, which requires investors to disclose how they handle sustainability risks and impacts."},
    {"type": "Frameworks", "q": "What is the 'EU Taxonomy'?", "a": "A classification system that defines which economic activities count as environmentally sustainable."},
    {"type": "Frameworks", "q": "What is 'assurance' in sustainability reporting?", "a": "Independent checking — like an audit — that reported ESG data is reliable."},
    {"type": "Frameworks", "q": "What is the difference between 'limited' and 'reasonable' assurance?", "a": "Limited gives moderate confidence ('nothing came to our attention'); reasonable is a higher level, closer to a full financial audit."},
    {"type": "Frameworks", "q": "What is the 'TNFD'?", "a": "The Taskforce on Nature-related Financial Disclosures — a nature and biodiversity counterpart to the climate-focused TCFD."},
    {"type": "Frameworks", "q": "How does 'materiality' differ between GRI and the ISSB?", "a": "GRI uses impact materiality (the company's effect on the world); the ISSB uses financial materiality (effect on enterprise value)."},
    {"type": "Regulation", "q": "What is the UNFCCC?", "a": "The UN Framework Convention on Climate Change — the 1992 treaty under which the COP summits and the Paris Agreement sit."},
    {"type": "Regulation", "q": "What is 'Loss and Damage' in climate negotiations?", "a": "Support for countries already suffering unavoidable climate harm; a dedicated fund was agreed at COP27 (2022) and launched at COP28 (2023)."},
    {"type": "Regulation", "q": "What is the 'Global Stocktake'?", "a": "A periodic Paris Agreement review of collective progress toward its goals, the first of which concluded in 2023."},
    {"type": "Regulation", "q": "What does 'COP' stand for in climate summits?", "a": "Conference of the Parties — the annual UN climate meeting under the UNFCCC (Paris was COP21; Glasgow COP26)."},

    # ---- Extra top-up (variety) ----
    {"type": "GHG Protocol", "q": "Which scope covers emissions from employee commuting and business travel?", "a": "Scope 3 (value-chain emissions)."},
    {"type": "GHG Protocol", "q": "What is the difference between 'location-based' and 'market-based' Scope 2 accounting?", "a": "Location-based uses the average grid emissions where you are; market-based reflects the specific electricity you contractually buy (e.g. green tariffs)."},
    {"type": "Carbon Markets", "q": "What is the difference between a 'compliance' and a 'voluntary' carbon market?", "a": "Compliance markets are created by law/regulation (e.g. the EU ETS); voluntary markets let firms buy offsets by choice."},
    {"type": "Carbon Markets", "q": "What does 'additionality' mean for a carbon offset?", "a": "The emission cut would not have happened without the money from selling the offset — otherwise it's not a real extra reduction."},
    {"type": "LCA", "q": "What does 'cradle-to-gate' cover in an LCA?", "a": "From raw-material extraction up to the point the product leaves the factory — excluding use and disposal."},
    {"type": "LCA", "q": "What does 'cradle-to-grave' cover in an LCA?", "a": "The full life cycle — raw materials, manufacturing, distribution, use, and end-of-life disposal or recycling."},
    {"type": "SBTi", "q": "What does the SBTi require beyond just setting a net-zero date?", "a": "Deep near-term cuts (typically ~50% by 2030) on a 1.5°C-aligned pathway, not just a distant net-zero pledge."},
    {"type": "Climate Science", "q": "Roughly how much has global average temperature risen since pre-industrial times?", "a": "About 1.1–1.2°C."},
    {"type": "Climate Science", "q": "What is 'radiative forcing'?", "a": "The change in energy balance in the atmosphere caused by factors like greenhouse gases — positive forcing warms the planet."},
    {"type": "Climate Science", "q": "What is the difference between 'weather' and 'climate'?", "a": "Weather is short-term day-to-day conditions; climate is the long-term average pattern over decades."},
    {"type": "Frameworks", "q": "What is the 'CDP' (formerly Carbon Disclosure Project)?", "a": "A global system where companies and cities disclose environmental data — emissions, water, forests — to investors and buyers."},
    {"type": "Regulation", "q": "What is a 'feed-in tariff'?", "a": "A policy guaranteeing renewable-energy producers a set price for the electricity they feed into the grid, to encourage clean generation."},
    {"type": "Regulation", "q": "What is a 'carbon tax'?", "a": "A direct price charged per tonne of CO2 emitted, giving polluters a financial reason to cut emissions."},
    {"type": "Social", "q": "What is 'Scope 3' got to do with the social pillar?", "a": "Supply-chain (Scope 3) work often overlaps with social issues like labour rights and fair wages among suppliers."},
    {"type": "Governance", "q": "What is 'ESG-linked executive pay'?", "a": "Tying part of leaders' bonuses to hitting sustainability targets, aligning their incentives with ESG goals."},
]

# ---------------------------------------------------------------------------
# 3) PROGRESSIVE ESG "BOSS" CHALLENGES  (the final escalating round)
#    Each generator returns a dict describing a fresh, randomised challenge.
# ---------------------------------------------------------------------------

_BOARD_INITIATIVES = [
    "switching the company to 100% renewable electricity",
    "setting a science-based net-zero target for 2040",
    "measuring the full Scope 3 value-chain footprint",
    "phasing out single-use plastic packaging",
    "electrifying the entire delivery fleet",
    "putting an internal carbon price on every business decision",
    "investing in a supplier decarbonisation programme",
    "retrofitting all buildings for energy efficiency",
    "publishing a fully audited sustainability report",
    "cutting food waste to zero across operations",
]

_ESG_CONCEPTS = [
    "Scope 3 emissions",
    "double materiality",
    "additionality in carbon credits",
    "the difference between net zero and carbon neutral",
    "cap and trade",
    "a Life Cycle Assessment",
    "the EU carbon border tax (CBAM)",
    "science-based targets",
    "embodied carbon",
    "carbon leakage",
    "financed emissions",
    "a just transition",
    "the three emission scopes",
    "why 1.5°C matters",
]

_STAKEHOLDERS = [
    "a smallholder farmer", "a long-term pension fund investor", "a factory-floor worker",
    "a city mayor", "a climate regulator", "a Gen-Z consumer", "a supply-chain manager",
    "an Indigenous community leader", "a small-business owner", "an energy-company CEO",
    "a climate scientist", "a bank's risk officer",
]

_STAKEHOLDER_TOPICS = [
    "a new carbon tax", "the EU carbon border tax", "a company's net-zero pledge",
    "a wind farm being built nearby", "stricter emissions reporting rules",
    "a shift from fossil fuels to renewables", "a voluntary carbon-credit project",
    "a plan to cut Scope 3 emissions",
]

_ESG_TABOO = [
    ("Net zero", ["carbon", "emissions", "zero"]),
    ("Renewable energy", ["solar", "wind", "power"]),
    ("The circular economy", ["waste", "recycle", "reuse"]),
    ("Carbon credits", ["offset", "tonne", "tree"]),
    ("Climate change", ["warming", "temperature", "weather"]),
    ("Sustainability", ["green", "future", "planet"]),
    ("A carbon footprint", ["carbon", "measure", "reduce"]),
    ("Greenwashing", ["fake", "claim", "misleading"]),
]

_ESG_DILEMMAS = [
    "Should heavy-emitting companies be allowed to use carbon offsets at all?",
    "Is nuclear power a climate solution or a climate risk?",
    "Should rich nations pay poorer nations for climate damage?",
    "Are ESG ratings trustworthy enough to guide investment?",
    "Should we prioritise cutting emissions now or removing carbon later?",
    "Is a carbon tax fairer than a cap-and-trade market?",
    "Should companies be legally forced to report Scope 3 emissions?",
    "Is 'degrowth' a serious answer to the climate crisis, or a dangerous one?",
]

_ESG_PROBLEMS = [
    "cutting a factory's Scope 1 emissions",
    "reducing plastic in product packaging",
    "decarbonising a delivery fleet",
    "greening a company's electricity supply",
    "reducing food waste in a supply chain",
    "improving suppliers' ESG performance",
    "making an old office building energy-efficient",
    "engaging employees in a sustainability goal",
]


def challenge_boardroom_pitch():
    initiative = random.choice(_BOARD_INITIATIVES)
    return {
        "name": "The Boardroom Pitch",
        "icon": "📊",
        "brief": f"You are the Chief Sustainability Officer pitching **{initiative}**.",
        "task": f"Speak for 60 seconds persuading a sceptical, cost-focused board to approve {initiative}. Lead with the business case, not guilt.",
        "trains": "Executive persuasion, linking sustainability to value, and confidence under pushback.",
        "difficulty": 1,
    }


def challenge_explain_simply():
    concept = random.choice(_ESG_CONCEPTS)
    return {
        "name": "Explain It Simply",
        "icon": "🧒",
        "brief": f"Explain **{concept}** to a curious 10-year-old.",
        "task": f"For 60 seconds, explain {concept} using plain words, everyday examples, and zero jargon. If you catch yourself using a buzzword, stop and say it a simpler way.",
        "trains": "Deep understanding, clarity, and stripping out jargon — the true test of expertise.",
        "difficulty": 2,
    }


def challenge_stakeholder_lens():
    who = random.choice(_STAKEHOLDERS)
    topic = random.choice(_STAKEHOLDER_TOPICS)
    return {
        "name": "The Stakeholder Lens",
        "icon": "🎭",
        "brief": f"Become **{who}**.",
        "task": f"For 60 seconds, react to **{topic}** entirely from the perspective, worries, and hopes of {who}. Make us feel their real stake in it.",
        "trains": "Empathy mapping, seeing ESG trade-offs from every side, and audience awareness.",
        "difficulty": 2,
    }


def challenge_jargon_taboo():
    topic, banned = random.choice(_ESG_TABOO)
    return {
        "name": "Jargon Taboo",
        "icon": "🚫",
        "brief": f"Explain **{topic}**.",
        "task": f"Talk about {topic} for 60 seconds without ever saying: **{', '.join(banned)}**. If you slip, acknowledge it and push on.",
        "trains": "Escaping buzzword autopilot and finding fresh, precise ways to explain ESG.",
        "difficulty": 3,
    }


def challenge_green_debate():
    dilemma = random.choice(_ESG_DILEMMAS)
    return {
        "name": "The Green Debate",
        "icon": "⚖️",
        "brief": f"Dilemma: **{dilemma}**",
        "task": f"Take a clear side and argue it hard for ~40 seconds — then spend the last ~20 seconds fairly steelmanning the opposite view. Commit, then show you understand both sides.",
        "trains": "Structured argument, nuance, and holding two viewpoints without waffling.",
        "difficulty": 3,
    }


def challenge_rapid_solutions():
    problem = random.choice(_ESG_PROBLEMS)
    return {
        "name": "Rapid-Fire Solutions",
        "icon": "⚡",
        "brief": f"Challenge: **{problem}**.",
        "task": f"Fire off as many *distinct* one-sentence ideas for {problem} as you can in 60 seconds — no repeats, no 'um'. Every sentence must start with a different word than the last.",
        "trains": "Idea fluency, solution thinking, and filler-word suppression under time pressure.",
        "difficulty": 3,
    }


# All boss challenges, roughly ordered by difficulty.
BOSS_CHALLENGES = [
    challenge_boardroom_pitch,
    challenge_explain_simply,
    challenge_stakeholder_lens,
    challenge_jargon_taboo,
    challenge_green_debate,
    challenge_rapid_solutions,
]


def pick_boss_challenge(level: int):
    """Higher level → bias toward harder challenges for progressive difficulty."""
    if level <= 2:
        pool = BOSS_CHALLENGES[:3]
    elif level <= 5:
        pool = BOSS_CHALLENGES[1:5]
    else:
        pool = BOSS_CHALLENGES[2:]
    return random.choice(pool)()


# ---------------------------------------------------------------------------
# 4) SPEAKING COACH — delivery technique (topic-neutral, still useful)
# ---------------------------------------------------------------------------

TONGUE_TWISTERS = [
    "Red leather, yellow leather, red leather, yellow leather.",
    "She sells seashells by the seashore.",
    "Peter Piper picked a peck of pickled peppers.",
    "Unique New York, unique New York, you know you need unique New York.",
    "The lips, the teeth, the tip of the tongue.",
    "A proper copper coffee pot.",
    "Six sticky skeletons sat and swayed.",
    "Toy boat, toy boat, toy boat.",
    "Which witch wished which wicked wish?",
    "Betty bought a bit of better butter.",
    "How much wood would a woodchuck chuck if a woodchuck could chuck wood?",
    "Fresh fried fish, fish fresh fried.",
]

VOICE_WARMUPS = [
    ("🌬️ Diaphragm breathing (30s)", "Sit tall. Inhale through the nose for 4 counts so your belly — not your chest — expands. Hold 2. Exhale slowly through pursed lips for 6. Repeat. This is the engine of a strong, steady voice."),
    ("🎵 The Siren (20s)", "On an 'ooo' sound, glide your pitch smoothly from your lowest note up to your highest and back down, like a slow siren. It stretches your full vocal range and warms the cords gently."),
    ("💆 Lip trills / 'brrr' (20s)", "Let your lips flutter as you hum a tune (like blowing a raspberry with sound). Releases tension in the lips and jaw and evens out airflow — a singer's secret."),
    ("🗣️ Over-articulate (30s)", "Read a tongue twister three times: first ridiculously slow and exaggerated, then medium, then fast but still crisp. Precision first, speed second."),
    ("😮 Big yawn-sigh (10s)", "Yawn wide, then sigh out on an open 'ahh'. Opens the throat and drops the larynx for a warmer, rounder tone."),
    ("💪 Neck & jaw roll (15s)", "Slowly roll your neck, then gently massage the jaw hinge and drop your jaw open-shut. Tension in the jaw chokes your resonance."),
]

COACH_CONFIDENCE = [
    "**Own the pause.** Silence feels long to you, powerful to them. When you finish a key point, stop for a full second. Pauses signal control, not uncertainty.",
    "**Kill the up-talk.** Ending sentences with a rising, question-like pitch makes statements sound unsure. Land your sentences with a firm, downward tone.",
    "**Plant your feet, open your chest.** Posture feeds your voice and your brain. Stand tall, shoulders back — you'll literally breathe better and sound more certain.",
    "**Slow down 20%.** Nervous speakers rush. Deliberate pace signals authority and gives your brain time to choose better words. Aim for ~130–150 words per minute.",
    "**Replace fillers with silence.** 'Um', 'uh', 'like', 'you know' are just pauses with noise. Train yourself to simply close your mouth and pause instead.",
    "**Speak in three-beat chunks.** Group ideas in threes ('faster, sharper, clearer'). The brain loves triads and they sound rehearsed and confident.",
]

COACH_EXCELLENCE = [
    "**Vary your pitch (prosody).** A monotone loses people in seconds. Consciously go higher on excitement, lower on gravity. Range = interest.",
    "**Use vocal dynamics.** Change volume too — drop to near-whisper to pull people in, rise to punch a point. Contrast is what the ear remembers.",
    "**Paint pictures, not lists.** 'A rusty red bicycle leaning on a cracked wall' beats 'an old bike.' Concrete, sensory nouns make you sound vivid and prepared.",
    "**Emphasise the operative word.** In every sentence one word carries the meaning. Hit it a touch harder and slower. 'I never *said* she stole it' changes meaning by stress alone.",
    "**Breathe at the punctuation, not mid-thought.** Plan your breaths at commas and full stops so ideas stay whole and you never sound out of air.",
    "**End on a line, not a fade.** Great speakers land a final, deliberate sentence and stop. Don't trail off — button it and be silent.",
]

COACH_VOICE_HEALTH = [
    "**Hydrate, don't clear.** Throat-clearing slams the vocal cords together. Instead, sip water or do a gentle 'hmm' hum to reset.",
    "**Warm up before you push.** Never launch into loud speaking cold — do the siren and lip-trills first. Cold cords strain and crack (the 'harsh voice' feeling).",
    "**Support from the belly, not the throat.** If your voice feels rough or tired, you're probably pushing from the throat. Power comes from breath support underneath.",
    "**Steam and rest for roughness.** For a genuinely harsh/hoarse voice, inhale steam from a bowl of hot water, avoid whispering (it strains more than normal talk), and rest the voice.",
    "**Open the throat with the 'yawn-sigh'.** If your tone is tight or grating, yawn to drop the larynx and speak on that open, relaxed space.",
    "**Avoid the vocal-fry crutch.** That low, creaky register at the end of sentences drains authority and tires the cords. Keep breath support up through the last word.",
]

SPEECH_STRUCTURE_TIP = (
    "**A reliable 3-part skeleton for any impromptu speech (P-E-P):**\n\n"
    "1. **Point** — State your one main idea in a single clear sentence.\n"
    "2. **Example / Explain** — Give one story, reason, or vivid picture that proves it.\n"
    "3. **Point again** — Restate the idea as a punchy, memorable closing line.\n\n"
    "When in doubt, answer three questions out loud: *What is it? Why does it matter? What should we do?*"
)

# ---------------------------------------------------------------------------
# 5) ESG LEARNING LIBRARY — descriptive, plain-language teaching for every
#    topic the quiz covers. Each item is {icon, title, body(markdown)}.
#    Rendered like the Speaking Coach tab: a stack of expanders.
# ---------------------------------------------------------------------------

ESG_LEARNING = [
    {
        "icon": "🌍",
        "title": "What is ESG? (start here)",
        "body": (
            "**ESG** stands for **Environmental, Social, and Governance** — three lenses for "
            "judging how responsibly a company behaves, beyond just its profits.\n\n"
            "- **E — Environmental:** climate emissions, energy, water, waste, pollution, nature.\n"
            "- **S — Social:** how a company treats people — employees, customers, suppliers, communities "
            "(safety, fair pay, human rights, diversity).\n"
            "- **G — Governance:** how the company is run — board independence, ethics, anti-corruption, "
            "transparency, and executive pay.\n\n"
            "The term became popular in a **2004 UN report called 'Who Cares Wins'**, which argued that "
            "these 'non-financial' issues actually affect a company's long-term financial health.\n\n"
            "**Everyday example:** two coffee brands sell the same latte. One pays farmers fairly, runs on "
            "renewable power, and has an honest board; the other hides its supply chain and pollutes a river. "
            "Same coffee — very different ESG profile, and very different long-term risk.\n\n"
            "**Two words you'll hear constantly:**\n"
            "- **Materiality** — focusing on the ESG issues that *actually matter* for a specific business "
            "(a bank's biggest issue is different from a mine's).\n"
            "- **Greenwashing** — making a company *look* greener than it is. The antidote is measured, "
            "verified data — which is what the rest of this library is about."
        ),
    },
    {
        "icon": "🏭",
        "title": "The GHG Protocol & the Three Scopes",
        "body": (
            "To manage emissions you first have to **measure** them. The global rulebook for that is the "
            "**GHG Protocol** (from WRI and WBCSD). It splits a company's greenhouse-gas emissions into "
            "**three 'scopes'**:\n\n"
            "- **Scope 1 — Direct.** Emissions from sources the company *owns or controls*: fuel burned in "
            "its factories, boilers, and company cars. *Example: the diesel in a delivery van.*\n"
            "- **Scope 2 — Indirect energy.** Emissions from the *electricity, steam, heating, and cooling "
            "the company buys*. *Example: the coal-fired power behind the electricity lighting an office.*\n"
            "- **Scope 3 — Everything else in the value chain.** All *other* indirect emissions, both "
            "**upstream** (making the things you buy) and **downstream** (customers using what you sell). "
            "It has **15 categories** — 8 upstream, 7 downstream.\n\n"
            "**The big surprise:** for most companies, **Scope 3 is by far the largest** — often 70–90% of "
            "the total. A car maker's own factory (Scope 1 & 2) is tiny next to the petrol burned by every "
            "car it ever sold (Scope 3).\n\n"
            "**Scope 2 has two counting methods:** *location-based* (the average dirtiness of the local grid) "
            "and *market-based* (reflecting green-energy contracts a company actually buys).\n\n"
            "That's why Scope 3 is the hardest and the most important frontier in corporate climate action."
        ),
    },
    {
        "icon": "🔬",
        "title": "Carbon Accounting: turning activity into tonnes of CO2",
        "body": (
            "**Carbon accounting** is simply *bookkeeping for emissions*. The core formula is beautifully "
            "simple:\n\n"
            "> **Activity data × Emission factor = Emissions**\n\n"
            "- **Activity data** = how much you did (litres of diesel, kWh of electricity, km flown).\n"
            "- **Emission factor** = how much CO2e that activity releases per unit (e.g. ~2.5 kgCO2e per "
            "litre of diesel).\n\n"
            "*Example:* burn 1,000 litres of diesel × 2.5 kgCO2e/litre = **2.5 tonnes of CO2e**.\n\n"
            "**CO2e (carbon dioxide equivalent)** is the universal unit. Different gases trap different "
            "amounts of heat, so we convert them all into 'the CO2 that would cause the same warming' using "
            "each gas's **Global Warming Potential (GWP)**:\n"
            "- **Methane (CH4):** ~28× CO2 over 100 years (and ~80× over 20 years).\n"
            "- **Nitrous oxide (N2O):** ~265× CO2.\n"
            "- **SF6:** over 20,000× CO2 — the most potent of the common industrial gases.\n\n"
            "**A few housekeeping terms:**\n"
            "- **Base year** — the reference year you compare progress against.\n"
            "- **Organisational boundary** — deciding which parts of a group 'count' (via *equity share*, "
            "*financial control*, or *operational control*).\n"
            "- **Financed emissions** — for banks and investors, the emissions of the companies they lend "
            "to or invest in (measured using the **PCAF** methodology). For a bank, these dwarf its office "
            "footprint."
        ),
    },
    {
        "icon": "💱",
        "title": "Carbon Markets & Carbon Credits",
        "body": (
            "A **carbon market** puts a *price* on emitting greenhouse gases, so pollution has a cost and "
            "cutting it has a reward. There are two families:\n\n"
            "- **Compliance markets** — created by law. The flagship is the **EU Emissions Trading System "
            "(EU ETS)**, the world's first major carbon market (launched **2005**). It uses **'cap and "
            "trade'**: a *cap* limits total emissions, companies hold tradable *allowances*, and the cap "
            "**falls every year** — squeezing emissions down.\n"
            "- **Voluntary markets** — where companies *choose* to buy **carbon credits** to meet their own "
            "goals. Big standards include **Verra (VCS)** and the **Gold Standard**.\n\n"
            "**One carbon credit = one tonne of CO2e** reduced, avoided, or removed.\n\n"
            "**The golden rule is 'additionality':** a credit only counts if the reduction *would not have "
            "happened anyway* without the funding. Without additionality, offsets become greenwashing.\n\n"
            "**Carbon tax vs cap-and-trade** — two ways to price carbon:\n"
            "- A **carbon tax** fixes the *price* (you know the cost, not the total emissions).\n"
            "- **Cap-and-trade** fixes the *quantity* (you know the emissions cap, and the market sets the "
            "price).\n\n"
            "**Worth knowing:** **Article 6** of the Paris Agreement governs *international* carbon trading; "
            "**REDD+** funds forest protection in developing countries; **CORSIA** offsets growth in "
            "international aviation.\n\n"
            "*Good practice:* cut your own emissions first — use credits only for the residual you genuinely "
            "can't yet eliminate."
        ),
    },
    {
        "icon": "🧪",
        "title": "Life Cycle Assessment (LCA)",
        "body": (
            "A **Life Cycle Assessment (LCA)** measures a product's total environmental impact across its "
            "*entire life* — so you don't just move a problem from one stage to another. It follows "
            "**ISO 14040 and ISO 14044**.\n\n"
            "**The four phases:**\n"
            "1. **Goal & scope** — what are we studying, and how far?\n"
            "2. **Inventory (LCI)** — list every input and output (energy, materials, emissions, waste).\n"
            "3. **Impact assessment (LCIA)** — translate those into impacts (climate, water, toxicity...).\n"
            "4. **Interpretation** — draw conclusions and spot the hotspots.\n\n"
            "**How far does it look? (the 'boundaries')**\n"
            "- **Cradle to grave** — raw materials → production → use → disposal (the full story).\n"
            "- **Cradle to gate** — raw materials → factory gate (stops before use/disposal).\n"
            "- **Cradle to cradle** — a circular version where waste becomes new input.\n\n"
            "**The functional unit** is the fair basis of comparison — e.g. '1 litre of milk delivered to a "
            "shop', so you compare *service delivered*, not just 'a carton'.\n\n"
            "**Two terms this unlocks:**\n"
            "- **Embodied carbon** — the emissions baked into *making* something (huge for concrete, steel, "
            "and buildings), separate from the emissions of *using* it.\n"
            "- **EPD (Environmental Product Declaration)** — a verified, LCA-based 'nutrition label' for a "
            "product's environmental impact (governed by ISO 14025).\n\n"
            "*Classic insight:* an LCA can reveal that a 'green' product is only green if you ignore how it's "
            "made — which is exactly the trap LCA is designed to catch."
        ),
    },
    {
        "icon": "🎯",
        "title": "Science Based Targets (SBTi) & Net Zero",
        "body": (
            "A climate target is only meaningful if it's big enough to matter. The **Science Based Targets "
            "initiative (SBTi)** checks that a company's goals are in line with real climate science — "
            "specifically, **limiting warming to 1.5°C**.\n\n"
            "SBTi was founded by **CDP, the UN Global Compact, WRI, and WWF**.\n\n"
            "**Companies set two kinds of target:**\n"
            "- **Near-term** — deep cuts over the next ~5–10 years (the part that actually bends the curve now).\n"
            "- **Long-term / net-zero** — reaching net zero by **no later than 2050**.\n\n"
            "**What 'net zero' really means (the strict version):** cut emissions **by around 90%** across "
            "all scopes, then *neutralise only the small residual ~10%* with permanent carbon removals. It is "
            "**not** 'carry on emitting and buy offsets'.\n\n"
            "- **Carbon neutral** usually = balancing emissions with offsets (weaker, often CO2-only).\n"
            "- **Net zero** = deep, science-based cuts across the whole value chain first (stronger).\n\n"
            "**A key rule:** if **Scope 3 is 40% or more** of a company's total emissions, it *must* set a "
            "Scope 3 target too — no hiding the biggest slice.\n\n"
            "*Rule of thumb:* **reduce first, remove later, offset last.** Real reductions beat clever accounting."
        ),
    },
    {
        "icon": "📚",
        "title": "Disclosure Frameworks (GRI, SASB, TCFD, ISSB, CSRD, BRSR)",
        "body": (
            "There are many 'alphabet-soup' frameworks for *reporting* ESG. Here's the map:\n\n"
            "- **GRI (Global Reporting Initiative)** — the most widely used; focuses on a company's "
            "**impacts on the world** (people, economy, environment). Multi-stakeholder.\n"
            "- **SASB** — **industry-specific**, **financially material** topics for investors. Now folded "
            "into the ISSB.\n"
            "- **TCFD (Task Force on Climate-related Financial Disclosures)** — climate risk reporting built "
            "on **four pillars: Governance, Strategy, Risk Management, and Metrics & Targets.** Its work is "
            "now carried on by the ISSB.\n"
            "- **ISSB (International Sustainability Standards Board)** — under the IFRS Foundation; in **2023** "
            "it issued **IFRS S1** (general sustainability) and **IFRS S2** (climate) — a global baseline.\n"
            "- **CSRD** — the EU's **Corporate Sustainability Reporting Directive**, which uses the **ESRS** "
            "standards and the principle of **double materiality**.\n"
            "- **BRSR** — India's **Business Responsibility and Sustainability Report**, required by **SEBI** "
            "for the **top 1,000 listed companies**, based on the **nine NGRBC principles**.\n"
            "- **CDP** — a global disclosure *platform* (formerly the 'Carbon Disclosure Project') where "
            "companies report climate, water, and forests data.\n\n"
            "**The one big idea — double materiality:**\n"
            "- **Financial materiality** — how sustainability issues affect the *company* (outside-in).\n"
            "- **Impact materiality** — how the *company* affects the world (inside-out).\n\n"
            "GRI leans on impact; the ISSB leans on financial; **CSRD asks for both.**"
        ),
    },
    {
        "icon": "📜",
        "title": "Key Regulations & Global Agreements",
        "body": (
            "**The climate treaties:**\n"
            "- **Kyoto Protocol (1997)** — the first treaty with *binding* emission cuts for developed "
            "countries.\n"
            "- **Paris Agreement (2015, agreed at COP21)** — nearly every country agreed to hold warming "
            "**well below 2°C** and pursue **1.5°C**. Each country sets its own pledge, called an **NDC "
            "(Nationally Determined Contribution)**, and strengthens it over time.\n"
            "- **COP** = the annual UN climate 'Conference of the Parties' (Paris was COP21; Glasgow COP26).\n\n"
            "**The maths of net zero:** to stay near 1.5°C, global emissions need to reach **net zero "
            "around 2050**. **India has pledged net zero by 2070** (announced at COP26).\n\n"
            "**The EU CBAM (Carbon Border Adjustment Mechanism):** a carbon price charged on **imports** of "
            "certain carbon-heavy goods — **cement, iron & steel, aluminium, fertilisers, electricity, and "
            "hydrogen**. Its purpose is to stop **'carbon leakage'** — companies simply moving dirty "
            "production to countries with weaker climate rules. A transitional (reporting-only) phase began "
            "in **October 2023**, with charges phasing in from **2026**.\n\n"
            "**Why it all connects:** treaties set the *goal*, carbon markets and CBAM set the *price*, the "
            "GHG Protocol and LCA provide the *measurement*, SBTi checks the *ambition*, and the disclosure "
            "frameworks make companies *show their work*."
        ),
    },
    {
        "icon": "📖",
        "title": "Quick Glossary — must-know terms",
        "body": (
            "- **CO2e** — carbon dioxide equivalent; the common unit for all greenhouse gases.\n"
            "- **GWP** — Global Warming Potential; how much heat a gas traps vs CO2 (usually over 100 years).\n"
            "- **Scopes 1 / 2 / 3** — direct / purchased-energy / value-chain emissions.\n"
            "- **Emission factor** — converts an activity into emissions.\n"
            "- **Carbon credit / offset** — one tonne of CO2e reduced, avoided, or removed elsewhere.\n"
            "- **Additionality** — the reduction wouldn't have happened without the funding.\n"
            "- **Cap and trade** — a falling cap on emissions with tradable allowances.\n"
            "- **Carbon leakage** — emissions escaping to regions with weaker rules.\n"
            "- **LCA** — Life Cycle Assessment of a product's full environmental impact.\n"
            "- **Embodied carbon** — emissions from *making* a product, not using it.\n"
            "- **Net zero** — deep cuts (~90%) plus removal of the small residual.\n"
            "- **Carbon neutral** — balancing emissions with offsets (a weaker claim).\n"
            "- **Double materiality** — financial impact *on* the company **and** the company's impact "
            "*on* the world.\n"
            "- **Just transition** — a fair shift to a low-carbon economy for affected workers.\n"
            "- **Greenwashing** — overstating how green something is.\n"
            "- **NDC** — a country's Paris Agreement climate pledge.\n"
            "- **Financed emissions** — the emissions of what a bank or investor funds."
        ),
    },
]
