// Helper to get preferred language (Japanese > English)
function getLang(obj) {
    if (!obj) return '';
    if (typeof obj === 'string') return obj;
    return obj.ja || obj.en || '';
}

// Helper to get English if available (for academic context)
function getEn(obj) {
    if (!obj) return '';
    if (typeof obj === 'string') return obj;
    return obj.en || obj.ja || '';
}

document.addEventListener('DOMContentLoaded', () => {
    if (typeof researcherData === 'undefined') {
        console.error('Data not loaded');
        return;
    }

    const data = researcherData.map(item => item.merge || item);

    // --- Profile Data ---
    // Use manualProfile if available, otherwise fallback to JSONL
    if (typeof manualProfile !== 'undefined') {
        const heroTitle = document.querySelector('.hero h1');
        const heroDesc = document.querySelector('.hero p');
        if (heroTitle) {
            heroTitle.textContent = `${manualProfile.name.en} (${manualProfile.name.ja})`;
        }
        if (heroDesc) {
            // Construct bio from affiliations and keywords
            const mainAffiliation = manualProfile.affiliations[0].en;
            const keywords = manualProfile.keywords.map(k => k.en).join(', ');
            heroDesc.innerHTML = `${mainAffiliation}<br>Specializing in ${keywords}`;
        }
    } else {
        const profile = data.find(item => item.type === 'researchers' || (item.family_name && item.given_name));
        if (profile) {
            // Update Hero if on index page
            const heroTitle = document.querySelector('.hero h1');
            if (heroTitle) {
                const nameJa = `${getLang(profile.family_name)} ${getLang(profile.given_name)}`;
                const nameEn = `${getEn(profile.given_name)} ${getEn(profile.family_name)}`;
                heroTitle.textContent = `${nameEn} (${nameJa})`;
            }
        }
    }

    // --- Affiliations ---
    const affiliationsList = document.getElementById('affiliations-list');
    if (affiliationsList) {
        affiliationsList.innerHTML = ''; // Clear existing
        if (typeof manualProfile !== 'undefined' && manualProfile.affiliations) {
            manualProfile.affiliations.forEach(item => {
                const li = document.createElement('li');
                li.className = 'mb-4';
                li.innerHTML = `<strong>${item.en}</strong><br>${item.ja}`;
                affiliationsList.appendChild(li);
            });
        } else {
            const affiliations = data.filter(item => item.type === 'research_experience' && item.display === 'disclosed')
                .sort((a, b) => (b.from_date || '').localeCompare(a.from_date || ''));

            // Filter for current affiliations (to_date is 9999 or empty)
            const currentAffiliations = affiliations.filter(item => item.to_date === '9999' || !item.to_date);

            currentAffiliations.forEach(item => {
                const li = document.createElement('li');
                li.className = 'mb-4';
                const affName = getEn(item.affiliation);
                const section = getEn(item.section);
                const job = getEn(item.job);
                li.innerHTML = `<strong>${affName}</strong><br>${section ? section + '<br>' : ''}${job}`;
                affiliationsList.appendChild(li);
            });
        }
    }

    // --- Education ---
    const educationList = document.getElementById('education-list');
    if (educationList) {
        const education = data.filter(item => item.type === 'education' && item.display === 'disclosed')
            .sort((a, b) => (b.from_date || '').localeCompare(a.from_date || ''));

        education.forEach(item => {
            const li = document.createElement('li');
            li.className = 'mb-4';
            const school = getEn(item.affiliation);
            const dept = getEn(item.department);
            const date = item.to_date ? item.to_date.substring(0, 4) : '';
            li.innerHTML = `<strong>${school}</strong><br>${dept}${date ? '<br>Completed: ' + date : ''}`;
            educationList.appendChild(li);
        });
    }

    // --- Research Interests ---
    const interestsContainer = document.getElementById('interests-container');
    if (interestsContainer) {
        const interests = data.filter(item => item.type === 'research_interests' && item.display === 'disclosed');
        interests.forEach(item => {
            const div = document.createElement('div');
            div.className = 'card text-center';
            div.innerHTML = `<h3>${getEn(item.keyword)}</h3>`;
            interestsContainer.appendChild(div);
        });
    }

    // --- Research Areas ---
    const areasContainer = document.getElementById('areas-container');
    if (areasContainer) {
        const areas = data.filter(item => item.type === 'research_areas' && item.display === 'disclosed');
        areas.forEach(item => {
            const div = document.createElement('div');
            div.className = 'card';
            div.innerHTML = `<h3>${getEn(item.discipline)}</h3><p>${getEn(item.research_field)}</p>`;
            areasContainer.appendChild(div);
        });
    }

    // --- Awards ---
    const awardsContainer = document.getElementById('awards-container');
    if (awardsContainer) {
        const awards = data.filter(item => item.type === 'awards' && item.display === 'disclosed')
            .sort((a, b) => (b.award_date || '').localeCompare(a.award_date || ''));

        awards.forEach(item => {
            const div = document.createElement('div');
            div.className = 'publication-item'; // Reuse style
            const name = getEn(item.award_name);
            const title = getEn(item.award_title);
            const date = item.award_date;
            div.innerHTML = `<div class="publication-title">${name}</div>
                             <div class="publication-authors">${title}</div>
                             <div class="publication-journal">${date}</div>`;
            awardsContainer.appendChild(div);
        });
    }

    // --- Publications ---
    const pubContainer = document.getElementById('publications-container');
    if (pubContainer) {
        pubContainer.innerHTML = ''; // Clear loading

        if (typeof manualPublications !== 'undefined') {
            const categories = [
                { key: 'international_journals', title: 'Original Articles (International)' },
                { key: 'domestic_journals', title: 'Original Articles (Domestic)' },
                { key: 'books', title: 'Books' },
                { key: 'domestic_conferences', title: 'Domestic Conferences / Invited Lectures' },
                { key: 'international_conferences', title: 'International Conferences' }
            ];

            categories.forEach(cat => {
                if (manualPublications[cat.key] && manualPublications[cat.key].length > 0) {
                    const sectionTitle = document.createElement('h3');
                    sectionTitle.className = 'mt-8 mb-4 text-xl font-bold text-slate-800 border-b pb-2';
                    sectionTitle.textContent = cat.title;
                    pubContainer.appendChild(sectionTitle);

                    manualPublications[cat.key].forEach(pubString => {
                        const div = document.createElement('div');
                        div.className = 'publication-item mb-4 p-4 bg-white rounded shadow-sm border border-slate-200';
                        div.innerHTML = `<p class="text-slate-700">${pubString}</p>`;
                        pubContainer.appendChild(div);
                    });
                }
            });

        } else {
            const publications = data.filter(item => (item.type === 'published_papers' || item.type === 'misc') && item.display === 'disclosed')
                .sort((a, b) => (b.publication_date || '').localeCompare(a.publication_date || ''));

            publications.forEach(item => {
                const div = document.createElement('div');
                div.className = 'publication-item';

                const title = getEn(item.paper_title);
                const journal = getEn(item.publication_name);
                const date = item.publication_date;

                let authors = '';
                if (item.authors && item.authors.en) {
                    authors = item.authors.en.map(a => a.name).join(', ');
                } else if (item.authors && item.authors.ja) {
                    authors = item.authors.ja.map(a => a.name).join(', ');
                }

                const type = item.type === 'published_papers' ? 'Paper' : 'Misc';

                // Links
                let linksHtml = '';
                if (item.see_also) {
                    item.see_also.forEach(link => {
                        linksHtml += `<a href="${link['@id']}" target="_blank" class="tag">${link.label}</a>`;
                    });
                } else if (item.identifiers && item.identifiers.doi) {
                    linksHtml += `<a href="https://doi.org/${item.identifiers.doi[0]}" target="_blank" class="tag">DOI</a>`;
                }

                div.innerHTML = `
                <div class="publication-title">${title}</div>
                <div class="publication-authors">${authors}</div>
                <div class="publication-journal">${journal} (${date}) <span style="float:right; font-size: 0.8rem; color: #94a3b8;">${type}</span></div>
                <div class="mt-4">${linksHtml}</div>
            `;
                pubContainer.appendChild(div);
            });
        }
    }
});
