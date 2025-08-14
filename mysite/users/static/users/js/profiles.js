document.addEventListener('DOMContentLoaded', () => {
  const loadingDiv = document.getElementById('loading')
  const profileListDiv = document.getElementById('profileList')
  const profileListDjangoDiv = document.getElementById('profileList_django')
  const refreshBtn = document.getElementById('refreshBtn')
  function showLoading() {
    loadingDiv.classList.remove('d-none')
  }

  function hideLoading() {
    loadingDiv.classList.add('d-none')
  }

  function renderProfiles(profiles) {
    try {
      profileListDiv.innerHTML = ''
      if (!profiles || !Array.isArray(profiles)) {
        throw new Error('資料格式錯誤')
      }

      if (profiles.length === 0) {
        throw new Error('無公開履歷資料')
      }

      profileListDiv.innerHTML = profiles
        .map(
          (profile) => `
                <div class="card profile-card" style="width: 14rem;">
                    <a href="${
                      profile.slug
                    }" class="text-decoration-none text-dark">
                        <img src="${
                          profile.avatar || '/media/avatars/default.png'
                        }" 
                             class="card-img-top profile-avatar" alt="avatar">
                        <div class="card-body">
                            <h5 class="card-title">${profile.masked_name}</h5>
                            <p class="card-text">${
                              profile.education || '未填寫學歷'
                            }</p>
                        </div>
                    </a>
                </div>
            `
        )
        .join('')
    } catch (error) {
      profileListDiv.innerHTML = `<p class="text-danger">${error.message}</p>`
    }
  }

  function renderProfiles_django(profiles) {
    try {
      if (!profiles || !Array.isArray(profiles)) {
        throw new Error('資料格式錯誤')
      }

      if (profiles.length === 0) {
        throw new Error('無公開履歷資料')
      }

      profileListDjangoDiv.innerHTML = profiles
        .map(
          (profile) => `
                <div class="card profile-card" style="width: 14rem;">
                    <a href="${
                      profile.slug
                    }" class="text-decoration-none text-dark">
                        <img src="${
                          profile.avatar || '/media/avatars/default.png'
                        }" 
                             class="card-img-top profile-avatar" alt="avatar">
                        <div class="card-body">
                            <h5 class="card-title">${profile.masked_name}</h5>
                            <p class="card-text">${
                              profile.education || '未填寫學歷'
                            }</p>
                        </div>
                    </a>
                </div>
            `
        )
        .join('')
    } catch (error) {
      profileListDiv.innerHTML = `<p class="text-danger">${error.message}</p>`
    }
  }

  async function main() {
    showLoading()
    const profile = fetchData('/api/public-profiles/')
      .then((profiles) => {
        renderProfiles(profiles)
      })
      .catch(() => {
        profileListDiv.innerHTML = `<p class="text-danger">無法載入公開履歷資料</p>`
      })

    const profiles_django = fetchData('/api/original-public-profiles/')
      .then((profiles) => {
        renderProfiles_django(profiles)
      })
      .catch(() => {
        profileListDiv.innerHTML = `<p class="text-danger">無法載入公開履歷資料</p>`
      })

    Promise.allSettled([profile, profiles_django]).then(() => {
      hideLoading()
    })
  }

  main()

  refreshBtn.addEventListener('click', () => {
    profileListDiv.innerHTML = ''
    profileListDjangoDiv.innerHTML = ''
    main()
  })
})
