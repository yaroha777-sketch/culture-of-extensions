// Vercel Serverless Function — writes website leads directly into Notion CRM
// Env vars required (set in Vercel Project Settings → Environment Variables):
//   NOTION_TOKEN        — Internal Integration Secret from notion.so/my-integrations
//   NOTION_DATA_SOURCE  — the CRM data source id (pre-filled below, override if needed)

const DATA_SOURCE_ID = process.env.NOTION_DATA_SOURCE || "1ef26508-aa47-484a-a875-6f9f19f4acf7";

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', 'https://www.cultureofextensions.com');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const token = process.env.NOTION_TOKEN;
  if (!token) {
    console.error('NOTION_TOKEN missing — lead not saved to Notion');
    return res.status(200).json({ ok: true, notion: false, reason: 'not_configured' });
  }

  try {
    const { name, phone, page } = req.body || {};
    if (!name || !phone) return res.status(400).json({ error: 'name and phone required' });

    const notionRes = await fetch('https://api.notion.com/v1/pages', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        parent: { data_source_id: DATA_SOURCE_ID },
        properties: {
          'Имя клиента': { title: [{ text: { content: name } }] },
          'Телефон': { phone_number: phone },
          'Источник': { select: { name: 'Сайт' } },
          'Статус': { select: { name: 'Новая заявка' } },
          'Услуга': { multi_select: [{ name: 'Консультация' }] },
          'Мастер': { select: { name: 'Lana' } },
          'Заметки': { rich_text: [{ text: { content: `Заявка с сайта (concierge chat)${page ? ' — ' + page : ''}` } }] }
        }
      })
    });

    if (!notionRes.ok) {
      const err = await notionRes.text();
      console.error('Notion API error:', notionRes.status, err);
      return res.status(200).json({ ok: true, notion: false, reason: 'notion_error' });
    }

    return res.status(200).json({ ok: true, notion: true });
  } catch (err) {
    console.error('Lead handler error:', err);
    return res.status(200).json({ ok: true, notion: false, reason: 'exception' });
  }
}
