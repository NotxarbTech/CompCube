function copyToClip(link) {
    navigator.clipboard.writeText(document.location.origin + link);
    alert("Share link copied to clipboard");
}