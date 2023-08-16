
import React from 'react';
import ReactMarkdown from 'react-markdown';
import { fetchMarkdownContent } from '../utils/api';

function MarkdownPage({ markdownContent }) {
  return (
    <div >
      <ReactMarkdown>{markdownContent}</ReactMarkdown>
    </div>
  );
}

export async function getServerSideProps() {
  const markdownContent = await fetchMarkdownContent();
  return { props: { markdownContent } };
}

export default MarkdownPage;