document.getElementById('show-navigate-panel-button').onclick = openNavigatePanel
document.getElementById('show-manage-panel-button').onclick = openManagePanel
document.getElementById('open-user-settings-button').onclick = openUserSettingsPanel

const navigatePanel = document.getElementById('navigate-panel')
const managePanel = document.getElementById('manage-panel')
const userSettingsPanel = document.getElementById('user-settings')
let navigatePanelIsOpen = false

function openNavigatePanel() {
    if (navigatePanel.getAttribute('data') === 'adaptive' && window.innerWidth <= 1024) {
        navigatePanel.className = 'panel show-panel right-panel right-panel-open-animation'
        navigatePanelIsOpen = true
    }
    if (navigatePanel.getAttribute('data') === 'no-adaptive') {
        navigatePanel.className = 'panel show-panel right-panel right-panel-open-animation'
        navigatePanelIsOpen = true
    }
}

function openManagePanel() {
    managePanel.className = 'panel show-panel left-panel left-panel-open-animation'
}

function openUserSettingsPanel() {
    userSettingsPanel.className = 'panel show-panel left-panel left-panel-open-animation'
}

document.getElementById('close-left-panel-button').onclick = function () {
    managePanel.className = 'panel show-panel left-panel left-panel-close-animation'

    managePanel.addEventListener('animationend', function listener(e) {
        managePanel.className = 'panel left-panel'
        managePanel.removeEventListener(e.type, listener)
    })
}

document.getElementById('close-right-panel-button').onclick = closeNavigatePanel

function closeNavigatePanel() {
    navigatePanel.className = 'panel show-panel right-panel right-panel-close-animation'

    navigatePanel.addEventListener('animationend', function listener(e) {
        navigatePanel.className = 'panel right-panel'
        navigatePanelIsOpen = false
        navigatePanel.removeEventListener(e.type, listener)
    })
}

document.getElementById('close-user-settings-button').onclick = function () {
    userSettingsPanel.className = 'panel show-panel left-panel left-panel-close-animation'

    userSettingsPanel.addEventListener('animationend', function listener(e) {
        userSettingsPanel.className = 'panel left-panel'
        userSettingsPanel.removeEventListener(e.type, listener)
    })
}

const searchBar = document.getElementById('search-bar')
const panelSearchBar = document.getElementById('panel-search-bar')

searchBar.addEventListener('input', function (e) {
    panelSearchBar.value = searchBar.value
})

panelSearchBar.addEventListener('input', function (e) {
    searchBar.value = panelSearchBar.value
})

$(window).on('resize', function () {
    if (navigatePanelIsOpen && navigatePanel.getAttribute('data') === 'adaptive' && window.innerWidth > 1024) {
        closeNavigatePanel()
    }
});