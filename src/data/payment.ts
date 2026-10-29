// Ödeme modeli — "Tasarrufa Dayalı Faizsiz Finansman Sistemi" konumlandırması.
// Bankasız · Faizsiz · Kefilsiz · 60 Ay Vade. Pazarlama odaklı, doğru bilgiyle.
// [DOĞRULANACAK: TDFFS'nin kooperatif yapısıyla hukuki/finansal ilişkisi avukat onayı gerektirir]

export const payment = {
  eyebrow: "Tasarrufa Dayalı Faizsiz Finansman Sistemi",
  title: "Banka yok. Faiz yok.",
  accent: "Kefil yok.",
  lead:
    "Tasarruf esaslı, faizsiz bir modelle ev sahibi olursunuz; bankaya da kefile de gerek yok. 1 milyon TL peşinatın ardından ödemeniz 60 aya kadar sabit taksitlere bölünür, ara ödeme çıkmaz ve taksitiniz baştan sona değişmez. Ev ve araç takası da kabul edilir.",
  // Öne çıkan sayı bloğu
  headline: {
    downPayment: "1 Milyon TL Peşinat",
    installments: "60",
    installmentsLabel: "Ay Sabit Taksit",
    interest: "%0",
    interestLabel: "Faiz / Vade Farkı",
  },
  trio: ["Bankasız", "Faizsiz", "Kefilsiz"],
  cards: [
    {
      icon: "Percent",
      title: "60 Ay, Sıfır Faiz",
      text: "60 aya varan ödeme yapıyorsunuz, üstelik ne faiz ne vade farkı. Banka ya da kredi peşinde koşmanıza gerek yok.",
    },
    {
      icon: "Lock",
      title: "Sabit Taksit, Ara Ödeme Yok",
      text: "Bugün belirlenen taksitiniz 60 ay boyunca aynı kalır. Ne ara ödeme çıkar, ne balon taksit. Sürpriz yok.",
    },
    {
      icon: "TrendingDown",
      title: "Enflasyona Karşı Avantaj",
      text: "Taksitiniz sabit kaldığı için, para değer kaybettikçe ödemenizin gerçek yükü ay ay hafifler. Bugün yüksek gelen taksit, birkaç yıl sonra cebinizi çok daha az yorar.",
    },
    {
      icon: "Handshake",
      title: "Üye Maliyetine Konut",
      text: "Kooperatif kâr amacı gütmez. Araya müteahhit kârı girmediği için konutu maliyetine yakın bir fiyata alırsınız.",
    },
  ],
  // Dipnot kaldırıldı. Yeniden göstermek isterseniz buraya metni yazmanız
  // yeterli; boş veya tanımsızsa bölümde hiç render edilmez.
  note: "",
  cta: "WhatsApp'tan randevu alın",
};
