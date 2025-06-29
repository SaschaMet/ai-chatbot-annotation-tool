# AI Chatbot Annotation Tool

A web-based tool for annotating, reviewing, and managing AI-generated chatbot responses. Built with FastAPI and SQLite, it provides a modern UI for human-in-the-loop evaluation, error code tagging, and persistent storage of annotations. The tool is suitable for research, dataset curation, and quality assurance of conversational AI systems.

![AI Chatbot Annotation Tool Screenshot](docs/imgs/Screenshot%202025-06-29%20at%2011.38.17.png)

---

## Features

- **Modern Web UI**: Clean, responsive interface for reviewing and annotating chatbot conversations.
- **Annotation Workflow**: Mark responses as Pass/Fail, add free-text feedback, and assign error codes.
- **Pagination**: Navigate through multiple chat samples with previous/next controls.
- **Bulk Upload**: Import chat data as JSON for annotation.
- **Download/Export**: Download all annotated data as a JSON file (UI button, backend endpoint can be added).
- **Persistent Storage**: All annotations are saved in a local SQLite database.
- **REST API**: Endpoints for CRUD operations on annotations.
- **Error Code Support**: Tag each annotation with custom error codes for granular analysis.
- **Delete All**: Remove all annotations with a single click.
- **Markdown Rendering**: Bot responses are rendered with markdown support for rich formatting.

---

## Project Structure

```
├── pyproject.toml
├── uv.lock
├── README.md
├── data/
│   └── demo_traces.json
├── sqlite/
│   └── annotations.db
├── src/
│   ├── annotation_server.py
│   └── index.html
```

---

## Quick Start (Running Locally with uv)

1. **Install [uv](https://github.com/astral-sh/uv):**
   ```bash
   pip install uv
   ```
2. **Install dependencies:**
   ```bash
   uv sync
   ```
3. **Run the FastAPI server:**
   ```bash
   uv run src/annotation_server.py
   ```
4. **Open the app:**
   Visit [http://localhost:8475](http://localhost:8475) in your browser.

---

## Usage Guide

### Web UI

- **Upload JSON**: Click "Upload a JSON file" to import chat data. The file should be an array of objects with at least `query` and `response` fields. Optional fields: `id`, `pass`, `feedback`, `error_code`.
- **Annotate**: For each chat, review the query/response, enter feedback, select Pass/Fail, and optionally add error codes.
- **Pagination**: Use Prev/Next to navigate between samples.
- **Delete All**: Remove all annotations (button disables if no data).
- **Download**: Download all annotations (button, backend endpoint can be added if not present).

### Annotation Data Format

Each annotation object has the following fields:

```json
{
  "id": 1, // integer (optional, auto-assigned if missing)
  "query": "User input", // string
  "response": "Bot reply", // string
  "pass": true, // boolean (Pass/Fail)
  "feedback": "...", // string (free text)
  "error_code": "..." // string (optional error codes)
}
```

You can find a sample JSON file in `data/demo_traces.json`.

---

## API Endpoints

- `GET /` — Serve the annotation tool UI (`index.html`)
- `GET /annotations` — List all annotations as JSON
- `POST /save-annotation` — Save or update an annotation (expects JSON body)
- `POST /upload-json` — Bulk upload annotations (expects `{ "data": [...] }`)
- `DELETE /annotations` — Delete all annotations

---

## Database Schema

The SQLite table `annotations` has the following columns:

- `id` (INTEGER PRIMARY KEY)
- `query` (TEXT)
- `response` (TEXT)
- `pass` (BOOLEAN)
- `feedback` (TEXT)
- `error_code` (TEXT)

---

## Development & Customization

- **Backend**: Modify `src/annotation_server.py` to add new endpoints or logic.
- **Frontend**: Edit `src/index.html` for UI/UX changes. Uses [Pico.css](https://picocss.com/) and [marked.js](https://marked.js.org/) for styling and markdown rendering.
- **Database**: The SQLite file is stored at `sqlite/annotations.db`.

---

## Contributing

Pull requests and issues are welcome! Please open an issue to discuss major changes.

---

## License

MIT License. See [LICENSE](LICENSE) for details.
