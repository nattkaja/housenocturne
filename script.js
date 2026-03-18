/* ═══════════════════════════════════════════════════════════════════════════
   HOUSE NOCTURNE LABS — Interactive Features
   Copy buttons, progress bar, TOC highlighting
   ═══════════════════════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', function() {
  
  // ─────────────────────────────────────────────────────────────────────────
  // Progress Bar
  // ─────────────────────────────────────────────────────────────────────────
  const progressBar = document.querySelector('.progress-bar');
  
  if (progressBar) {
    window.addEventListener('scroll', function() {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrollPercent = (scrollTop / docHeight) * 100;
      progressBar.style.width = scrollPercent + '%';
    });
  }
  
  // ─────────────────────────────────────────────────────────────────────────
  // Copy to Clipboard
  // ─────────────────────────────────────────────────────────────────────────
  document.querySelectorAll('.copy-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      const codeBlock = this.closest('.code-block');
      const code = codeBlock.querySelector('code');
      const text = code.textContent;
      
      navigator.clipboard.writeText(text).then(function() {
        btn.textContent = 'Copied!';
        btn.classList.add('copied');
        
        setTimeout(function() {
          btn.textContent = 'Copy';
          btn.classList.remove('copied');
        }, 2000);
      }).catch(function(err) {
        console.error('Failed to copy:', err);
        btn.textContent = 'Failed';
        setTimeout(function() {
          btn.textContent = 'Copy';
        }, 2000);
      });
    });
  });
  
  // ─────────────────────────────────────────────────────────────────────────
  // Table of Contents Active State
  // ─────────────────────────────────────────────────────────────────────────
  const tocLinks = document.querySelectorAll('.toc__link');
  const sections = document.querySelectorAll('.tutorial__content h2[id], .tutorial__content h3[id]');
  
  if (tocLinks.length > 0 && sections.length > 0) {
    const observerOptions = {
      rootMargin: '-100px 0px -66%',
      threshold: 0
    };
    
    const observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          // Remove active from all
          tocLinks.forEach(function(link) {
            link.classList.remove('active');
          });
          
          // Add active to current
          const id = entry.target.getAttribute('id');
          const activeLink = document.querySelector('.toc__link[href="#' + id + '"]');
          if (activeLink) {
            activeLink.classList.add('active');
          }
        }
      });
    }, observerOptions);
    
    sections.forEach(function(section) {
      observer.observe(section);
    });
  }
  
  // ─────────────────────────────────────────────────────────────────────────
  // Simple Syntax Highlighting
  // ─────────────────────────────────────────────────────────────────────────
  document.querySelectorAll('.code-block code').forEach(function(block) {
    // Skip markdown blocks - they don't need highlighting and it breaks them
    if (block.classList.contains('language-markdown')) {
      return;
    }
    
    let html = block.innerHTML;
    
    // Skip if content looks like it might have complex nested structures
    // (YAML frontmatter, etc.) - these break with naive regex highlighting
    if (html.includes('---\n') || html.includes('description:')) {
      return;
    }
    
    // Escape HTML first (already done in the HTML)
    // Then apply highlighting
    
    // Strings (double and single quotes)
    html = html.replace(/(&quot;[^&]*&quot;|"[^"]*"|'[^']*')/g, '<span class="hljs-string">$1</span>');
    
    // Comments (# and //)
    html = html.replace(/(#[^\n<]*)/g, '<span class="hljs-comment">$1</span>');
    html = html.replace(/(\/\/[^\n<]*)/g, '<span class="hljs-comment">$1</span>');
    
    // Keywords
    const keywords = ['def', 'import', 'from', 'return', 'if', 'else', 'elif', 'for', 'while', 'try', 'except', 'with', 'as', 'async', 'await', 'True', 'False', 'None', 'function', 'const', 'let', 'var', 'new', 'this'];
    keywords.forEach(function(kw) {
      const regex = new RegExp('\\b(' + kw + ')\\b', 'g');
      html = html.replace(regex, '<span class="hljs-keyword">$1</span>');
    });
    
    // Numbers
    html = html.replace(/\b(\d+\.?\d*)\b/g, '<span class="hljs-number">$1</span>');
    
    // Function calls (word followed by parenthesis)
    html = html.replace(/\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(/g, '<span class="hljs-function">$1</span>(');
    
    block.innerHTML = html;
  });
  
});
