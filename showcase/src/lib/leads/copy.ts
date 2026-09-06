export const BOT_COPY = {
  welcome:
    "LeadFlow is a request desk for a small service studio. Send a structured brief and the team will follow up using the contact method you prefer.",
  about:
    "This is a personal portfolio demonstration of a Telegram lead bot with a lightweight CRM workflow. It is not a live client product and does not represent paid client work.",
  askName: "What is your full name?",
  askPhone: "What is the best phone number to reach you?",
  askCategory: "Which service are you looking for?",
  askDescription: "Briefly describe the project. A few sentences is enough.",
  askContact: "How should we contact you?",
  cancelled: "Request cancelled. You can start again from the menu whenever you like.",
  emptyRequests: "You have not submitted a request yet.",
  duplicate: (publicId: string) =>
    `A matching request is already in the queue as ${publicId}. I did not create a duplicate.`,
  success: (publicId: string) =>
    `Request ${publicId} is in the queue. An administrator will review it shortly.`,
  statusNotice: (publicId: string, status: string) =>
    `Update on ${publicId}: status is now ${status}.`,
};
