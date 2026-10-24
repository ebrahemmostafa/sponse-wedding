/*
  Everything you need to edit lives in this file.
  After changing the initials, rebuild the envelope:
    python tools/personalize_envelope.py --initials "Y&M" [--photo path/to/photo.jpg]
*/
window.INVITE = {
  couple: { one: "Youssef", two: "Malak" },

  // date + time of the wedding, with the Cairo offset
  date: "2027-04-15T19:00:00+02:00",
  timeZone: "Africa/Cairo",
  durationHours: 5,

  hero: {
    above: "With joy in our hearts",
    below: "invite you to celebrate our wedding",
  },

  // up to 3 photos for the photobooth strip (printed in black and white)
  photos: ["assets/photos/hands.jpg", "assets/photos/toast.jpg", "assets/photos/veil.jpg"],

  venue: {
    name: "Four Seasons Nile Plaza",
    address: "1089 Corniche El Nil, Garden City, Cairo",
    mapUrl: "https://maps.google.com/?q=Four+Seasons+Nile+Plaza+Cairo",
  },

  programme: [
    { time: "19:00", what: "Guests arrive" },
    { time: "19:30", what: "Katb El-Ketab" },
    { time: "20:30", what: "Zaffa & first dance" },
    { time: "22:00", what: "Dinner" },
  ],

  dressCode: {
    title: "Formal evening wear",
    note: "Kindly keep white for the bride.",
  },

  rsvp: {
    // WhatsApp number that receives replies, international format without "+"
    whatsapp: "201000000000",
    deadline: "2027-03-15",
  },

  closing: "We can't wait to celebrate with you",
};
