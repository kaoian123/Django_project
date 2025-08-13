document.addEventListener("DOMContentLoaded", () => {
    const loadingDiv = document.getElementById("loading");
    const profileListDiv = document.getElementById("profileList");

    function showLoading() {
        loadingDiv.classList.remove("d-none");
    }

    function hideLoading() {
        loadingDiv.classList.add("d-none");
    }
    function renderProfiles(profiles) {
        if (!profiles || profiles.length === 0) {
            profileListDiv.innerHTML = `<p class="text-muted">目前沒有使用者資料</p>`;
            return;
        }

        profileListDiv.innerHTML = profiles.map(profile => `
            <div class="card profile-card" style="width: 14rem;">
                <a href="${profile.slug}" class="text-decoration-none text-dark">
                    <img src="${profile.avatar || '/media/avatars/default.png'}" 
                         class="card-img-top profile-avatar" alt="avatar">
                    <div class="card-body">
                        <h5 class="card-title">${profile.masked_name}</h5>
                        <p class="card-text">${profile.education || '未填寫學歷'}</p>
                    </div>
                </a>
            </div>
        `).join('');
    }

    async function main() {
        try {
            showLoading();
            const API_URL = window.location.origin + "/api/public-profiles/";
            const profiles = await fetchData(API_URL);
            renderProfiles(profiles);
        } catch (error) {
            profileListDiv.innerHTML = `<p class="text-danger">無法載入公開履歷資料</p>`;
        } finally {
            hideLoading();
        }
    }

    main();
});
