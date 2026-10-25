/* Independent entry point: the two invitations never share styles or audio. */
(() => {
  const root = new URL('../', document.currentScript.src);
  const current = new URL(location.href);
  const isMaplePage = current.pathname.startsWith(new URL('maple/', root).pathname);
  if (!isMaplePage && current.searchParams.get('type') === 'maple') {
    const destination = new URL('maple/', root);
    destination.search = current.search;
    destination.hash = current.hash;
    location.replace(destination.href);
    return;
  }
  document.addEventListener('DOMContentLoaded', () => {
    const copyright = document.querySelector('footer .copyright');
    if (!copyright) return;
    const link = document.createElement('a');
    const destination = new URL(root);
    if (!isMaplePage) destination.searchParams.set('type', 'maple');
    link.href = destination.href;
    link.className = 'maple-secret-entry';
    link.setAttribute('aria-label', isMaplePage ? '일반 청첩장으로 돌아가기' : '메이플 청첩장 열기');
    const icon = document.createElement('span');
    icon.setAttribute('aria-hidden', 'true');
    link.append(icon);
    copyright.append(link);
  });
})();
