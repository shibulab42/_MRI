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

    // --- Research Overview (Home) ---
    const homeOverview = document.getElementById('home-research-overview-content');
    if (homeOverview && typeof manualProfile !== 'undefined' && manualProfile.research_interests) {
        if (typeof manualProfile.research_interests === 'string') {
            homeOverview.textContent = manualProfile.research_interests;
        } else {
            homeOverview.textContent = manualProfile.research_interests.en || manualProfile.research_interests.ja;
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

    // --- What's New ---
    const whatsNewList = document.getElementById('whats-new-list');
    if (whatsNewList) {
        fetch('news.txt')
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.text();
            })
            .then(text => {
                const lines = text.split('\n');
                let currentItem = null;

                const renderItem = (item) => {
                    if (!item) return;

                    const div = document.createElement('div');
                    div.className = 'news-item mb-4 pb-2 border-b border-gray-100 last:border-0';

                    let content = `<div class="text-sm text-gray-500 mb-1">${item.date} <span class="px-2 py-0.5 rounded text-xs ${item.category.includes('Award') ? 'bg-yellow-100 text-yellow-800' : 'bg-blue-100 text-blue-800'}">${item.category}</span></div>`;

                    // Main Title
                    content += `<p class="font-medium text-gray-800">${item.title}</p>`;

                    // Description / Citation / URL from subsequent lines
                    if (item.description) {
                        // Check if description has URL format: Text | URL
                        const descMatch = item.description.match(/^(.*?)\s*\|\s*(https?:\/\/.+?)\s*$/);
                        if (descMatch) {
                            const descText = descMatch[1];
                            const descUrl = descMatch[2];
                            content += `<a href="${descUrl}" target="_blank" class="block text-sm text-blue-600 hover:text-blue-800 mt-1">${descText}</a>`;
                        } else {
                            content += `<p class="text-sm text-gray-600 mt-1">${item.description}</p>`;
                        }
                    } else if (item.url) {
                        content += `<a href="${item.url}" target="_blank" class="block text-sm text-blue-600 hover:text-blue-800 mt-1">Link</a>`;
                    }

                    div.innerHTML = content;
                    whatsNewList.appendChild(div);
                };

                lines.forEach(line => {
                    if (!line.trim()) return;

                    // Format: YYYY.MM [Category] Title | URL (Optional on same line)
                    const match = line.match(/^(\d{4}\.\d{2})\s+\[(.*?)\]\s+(.*?)(?:\s*\|\s*(.*))?$/);

                    if (match) {
                        if (currentItem) renderItem(currentItem);

                        currentItem = {
                            date: match[1],
                            category: match[2],
                            title: match[3],
                            url: match[4],
                            description: ''
                        };
                    } else if (currentItem) {
                        if (currentItem.description) currentItem.description += ' ';
                        currentItem.description += line.trim();
                    }
                });

                if (currentItem) renderItem(currentItem);
            })
            .catch(error => {
                console.error('Error loading news:', error);
                whatsNewList.innerHTML = '<p class="text-gray-500">Latest updates loading...</p>';
            });
    }

    // --- Research Interests ---
    const interestsContainer = document.getElementById('interests-container');
    if (interestsContainer) {
        if (typeof manualProfile !== 'undefined' && manualProfile.research_interests) {
            // Use manual text description
            interestsContainer.className = 'card'; // Change from card-grid to single card

            let content = '';
            if (typeof manualProfile.research_interests === 'object') {
                content += `<p style="white-space: pre-wrap; line-height: 1.8; margin-bottom: 1.5rem;">${manualProfile.research_interests.ja}</p>`;
                content += `<hr style="border: 0; border-top: 1px solid #eee; margin: 1.5rem 0;">`;
                content += `<p style="white-space: pre-wrap; line-height: 1.8;">${manualProfile.research_interests.en}</p>`;
            } else {
                content = `<p style="white-space: pre-wrap; line-height: 1.8;">${manualProfile.research_interests}</p>`;
            }
            interestsContainer.innerHTML = content;
        } else {
            // Fallback to keywords from JSONL
            const interests = data.filter(item => item.type === 'research_interests' && item.display === 'disclosed');
            interests.forEach(item => {
                const div = document.createElement('div');
                div.className = 'card text-center';
                div.innerHTML = `<h3>${getEn(item.keyword)}</h3>`;
                interestsContainer.appendChild(div);
            });
        }
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
        awardsContainer.innerHTML = ''; // Clear existing

        if (typeof manualProfile !== 'undefined' && manualProfile.awards) {
            manualProfile.awards.forEach(award => {
                const div = document.createElement('div');
                div.className = 'publication-item mb-4 p-4 bg-white rounded shadow-sm border border-slate-200';
                div.innerHTML = `<p class="text-slate-700">${award}</p>`;
                awardsContainer.appendChild(div);
            });
        } else {
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
    }

    // --- Publications ---
    const pubContainer = document.getElementById('publications-container');
    if (pubContainer) {
        pubContainer.innerHTML = ''; // Clear loading

        if (typeof manualPublications !== 'undefined') {
            const categories = [
                { key: 'international_journals', title: 'Original Articles (International)', className: 'pub-int-journal' },
                { key: 'domestic_journals', title: 'Original Articles (Domestic)', className: 'pub-dom-journal' },
                { key: 'books', title: 'Books', className: 'pub-book' },
                { key: 'international_conferences', title: 'International Conferences', className: 'pub-int-conf' },
                { key: 'domestic_conferences', title: 'Domestic Conferences / Invited Lectures', className: 'pub-dom-conf' }
            ];

            categories.forEach(cat => {
                if (manualPublications[cat.key] && manualPublications[cat.key].length > 0) {
                    const sectionTitle = document.createElement('h3');
                    sectionTitle.className = 'mt-8 mb-4 text-xl font-bold text-slate-800 border-b pb-2';
                    sectionTitle.style.borderBottom = `3px solid ${getComputedStyle(document.documentElement).getPropertyValue('--accent-color')}`;
                    sectionTitle.textContent = cat.title;
                    pubContainer.appendChild(sectionTitle);

                    manualPublications[cat.key].forEach(pubString => {
                        const div = document.createElement('div');
                        div.className = `publication-card ${cat.className}`;
                        div.innerHTML = `<p class="publication-text">${pubString}</p>`;
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

// --- Lab Members Page ---
const collaboratorsContainer = document.getElementById('collaborators-container');
if (collaboratorsContainer && typeof manualProfile !== 'undefined' && manualProfile.lab_members) {
    collaboratorsContainer.innerHTML = '';
    manualProfile.lab_members.collaborators.forEach(member => {
        const div = document.createElement('div');
        div.className = 'member-card-small';
        if (typeof member === 'object') {
            let content = `<strong>${member.name_en} (${member.name_ja})</strong><br>${member.affiliation}`;
            if (member.url) {
                content += `<br><a href="${member.url}" target="_blank" class="text-blue-600 hover:text-blue-800 text-sm">ResearchMap</a>`;
            }
            div.innerHTML = `<p>${content}</p>`;
        } else {
            div.innerHTML = `<p>${member}</p>`;
        }
        collaboratorsContainer.appendChild(div);
    });
}

const mastersContainer = document.getElementById('masters-container');
if (mastersContainer && typeof manualProfile !== 'undefined' && manualProfile.lab_members) {
    mastersContainer.innerHTML = '';
    manualProfile.lab_members.masters.forEach(member => {
        const div = document.createElement('div');
        div.className = 'member-card-small';
        div.innerHTML = `<p>${member}</p>`;
        mastersContainer.appendChild(div);
    });
}

const undergradsContainer = document.getElementById('undergrads-container');
if (undergradsContainer && typeof manualProfile !== 'undefined' && manualProfile.lab_members) {
    undergradsContainer.innerHTML = '';
    manualProfile.lab_members.undergraduates.forEach(member => {
        const div = document.createElement('div');
        div.className = 'member-card-small';
        div.innerHTML = `<p>${member}</p>`;
        undergradsContainer.appendChild(div);
    });
}
