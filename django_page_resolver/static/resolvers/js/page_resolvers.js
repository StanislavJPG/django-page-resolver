function pageScrollToInstance() {
    const scrollToInstance = window.scrollToInstance;
    const prefix = "scroll-instance-";

    if (scrollToInstance) {
        const targetElement = document.querySelector(`.${prefix}${scrollToInstance}`);
        if (targetElement) {
            targetElement.scrollIntoView({behavior: "smooth", block: "start"});
        }
        setTimeout(() => {
            document.querySelectorAll(".fadeDiv").forEach(element => {
                element.classList.add("fade-remove");
                setTimeout(() => {
                    element.classList.remove("bg-warning-subtle");
                    element.classList.remove("fade-remove");
                }, 500);
            });
        }, 1000);
    }
}

["DOMContentLoaded", "htmx:afterSettle"].forEach(event =>
    document.addEventListener(event, pageScrollToInstance)
);