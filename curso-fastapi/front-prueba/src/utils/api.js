async function fetchMarkdownContent() {
  const response = await fetch('http://127.0.0.1:8000/markdown');  // Replace with your API URL
  const data = await response.text();
  return data;
}

export { fetchMarkdownContent };