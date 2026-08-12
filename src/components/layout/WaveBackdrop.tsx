/**
 * Site arka planı — logodaki dalga.
 *
 * Üç katman da `/brand/wave.webp`'tir: logonun altındaki dalganın kendisi,
 * hiç değiştirilmeden kesilmiş orijinal pikseller. Katmanlar farklı ölçek ve
 * yükseklikte, çok yavaş yatay salınımla akar; uçları hiçbir zaman ekrana
 * girmediği için ek/derz görünmez.
 *
 * Sabit (fixed) durur; içerik kaydıkça dalgalar yerinde kalır ve sayfaya
 * sakin bir "okyanus zemini" hissi verir. Bölüm zeminleri yarı saydam olduğu
 * için doku hafifçe görünür.
 *
 * Tamamen dekoratiftir: tıklama almaz, ekran okuyucuya görünmez.
 */
export function WaveBackdrop() {
  return (
    <div
      className="pointer-events-none fixed inset-0 -z-10 overflow-hidden"
      style={{
        // Buz mavisinden beyaza yıkama — sayfanın hiçbir yeri bembeyaz kalmaz
        backgroundImage:
          "linear-gradient(178deg, #ffffff 0%, #f4fcfd 16%, #e4f6fa 38%, #d2f0f6 58%, #e9f8fb 78%, #f8fdfe 100%)",
      }}
      aria-hidden="true"
    >
      {/* Üst yumuşak ışık */}
      <div className="absolute -top-1/4 left-1/2 h-[70vh] w-[120vw] -translate-x-1/2 rounded-full bg-[radial-gradient(closest-side,rgba(255,255,255,0.7),transparent)]" />

      {/* Katman 1 — en yüksek, en soluk */}
      <div className="absolute inset-x-0 top-[13%] h-[26vh] overflow-hidden">
        <span className="wave-ribbon wave-swell-slow absolute -left-[24%] top-0 h-full w-[152%] opacity-[0.18] blur-[2px]" />
      </div>

      {/* Katman 2 — orta */}
      <div className="absolute inset-x-0 top-[42%] h-[30vh] overflow-hidden">
        <span className="wave-ribbon wave-swell absolute -left-[38%] top-0 h-full w-[178%] opacity-[0.16] blur-[3px]" />
      </div>

      {/* Katman 3 — altta, en belirgin */}
      <div className="absolute inset-x-0 bottom-0 h-[34vh] overflow-hidden">
        <span className="wave-ribbon wave-swell-slow absolute -left-[16%] top-0 h-full w-[136%] opacity-[0.22] blur-[2px]" />
      </div>

      {/* Beyaza doğru yumuşak kapanış — dalgalar metnin altında kalır */}
      <div className="absolute inset-0 bg-[linear-gradient(180deg,rgba(255,255,255,0.42),rgba(255,255,255,0.12)_38%,rgba(255,255,255,0.34)_72%,rgba(255,255,255,0.6))]" />
    </div>
  );
}
