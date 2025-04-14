<p align="center">
  <a href="https://isoloops.vercel.app/">
    <img src="https://github.com/daniale93/isoloops/blob/main/frontend/public/isoloops-logo-transparent.png" alt="isoloops logo" width="200"/>
  </a>
</p>

<p align="center">
  <a href="https://isoloops.vercel.app/">🌐 Visit the isoloops Website</a>
</p>


# 🎶 isoloops

**isoloops** is an experimental data engineering project and music discovery tool designed to help producers find *sampleable* music moments—especially isolated percussion or vocal sections—from obscure Afro, Latin, funk, and world records.

This project showcases the use of modern data engineering tools and large language models (LLMs) to automate the discovery, enrichment, and presentation of unique musical samples.

---

## 🛠️ Project Pipeline (In Progress)

The architecture includes:

### 1. **Daily Artist Discovery (LLM + Airflow)**
- Uses an LLM to generate daily artist recommendations likely to have sample-worthy content
- Rotates through prompt variations for diversity
- Logs the LLM prompt to a Snowflake table
- This data will later be used to optimize prompts to find better songs
- Scheduled with daily Airflow DAGs -- from discovery to ingestion

### 2. **YouTube Search & Ranking**
- Searches YouTube for videos by the selected artists.
- Filters by duration (1–10 min), resolution, and engagement.
- These queries are also stored in order to improve track finding in Youtube

### 3. **Sample Detection & Metadata Extraction**
- Uses LLM to add sample metadata: type, description, genre, decade, and more

### 4. **Snowflake Data Warehouse**
- Stores raw, staging, and enriched song data.
- Tables: `SAMPLED_SONGS`, `SAMPLED_SONGS_STAGING`, `SAMPLED_SONGS_ENRICHED`

### 5. **API + Frontend (Vercel, React)**
- A lightweight Vercel-hosted API pulls from Snowflake
- Frontend lets users explore sampleable songs with filters and a "Surprise Me" feature

---

## 🚧 Status

- ✅ Initial pipeline built and automated via Airflow
- ✅ Data flows into Snowflake from LLM > YouTube > enrichment scripts
- ✅ Frontend MVP live with sample browser
- 🛠️ Enrichment automation still in progress (e.g. genre, artist, decade extraction)
- 🛠️ AI-powered sample section detection in exploration phase

---

## 📈 Next Steps

- [ ] Automate genre, sample type, and decade tagging using LLM during enrichment step
- [ ] Build admin dashboard for reviewing and approving samples
- [ ] Deploy outside Vercel for scale and customization
- [ ] Add social features like sharing or saving samples
- [ ] Implement a feedback loop where user likes and interactions teach the model which prompts and YouTube queries yield the best results

---

## 🙌 Why Sampling?

Sampling is at the heart of many genres, but finding usable, clean material is time-consuming. isoloops aims to streamline that process by combining musical intuition with scalable data engineering.

---

## 📬 Contact

Built by [Daniel Torres](https://www.linkedin.com/in/engdanieltorres/)  