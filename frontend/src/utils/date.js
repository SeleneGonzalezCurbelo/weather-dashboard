// src/utils/date.js
export function formattedDate(latest) {
    return new Intl.DateTimeFormat("es-ES", {
        weekday: "long",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
    }).format(new Date(latest.created_at));
}