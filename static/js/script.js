
document.getElementById('resume-form').addEventListener('input', function () {
    const form = new FormData(this);
    let preview = '';
    for (let [key, value] of form.entries()) {
        preview += `<h3>${key}</h3><p>${value}</p>`;
    }
    document.getElementById('preview').innerHTML = preview;
});
