import { useState } from "react";
import {
  Shield,
  AlertTriangle,
  Loader2,
  Info,
  Sparkles
} from "lucide-react";

import { FeatureDisplay } from "./components/FeatureDisplay";

export default function App() {

  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  // ANALYZE URL
  const handleAnalyze = async () => {

    if (!url.trim()) {
      alert("Please enter URL");
      return;
    }

    setLoading(true);

    try {

      const response = await fetch(
        "http://localhost:5000/predict",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ url })
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data?.error || "Prediction failed");
      }

      setResult(data);

    } catch (error: any) {

      alert(error?.message || "Backend connection error");

    } finally {

      setLoading(false);

    }
  };

  // RESET
  const handleReset = () => {
    setUrl("");
    setResult(null);
  };

  return (

    <div className="min-h-screen relative overflow-hidden bg-black">

      {/* BACKGROUND */}
      <div className="absolute inset-0">

        {/* Main Gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-[#0f2027] via-[#203a43] to-[#2c5364]" />

        {/* Glow Effects */}
        <div className="absolute top-[-120px] left-[-120px] w-[400px] h-[400px] bg-sky-400 opacity-20 blur-[120px] rounded-full" />

        <div className="absolute bottom-[-120px] right-[-120px] w-[400px] h-[400px] bg-blue-500 opacity-20 blur-[120px] rounded-full" />

        {/* Extra Glow */}
        <div className="absolute top-[40%] left-[35%] w-[300px] h-[300px] bg-cyan-300 opacity-10 blur-[100px] rounded-full" />

        {/* Grid Overlay */}
        <div
          className="absolute inset-0 opacity-10"
          style={{
            backgroundImage:
              "linear-gradient(rgba(255,255,255,0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.08) 1px, transparent 1px)",
            backgroundSize: "40px 40px",
          }}
        />

      </div>

      {/* MAIN CONTENT */}
      <div className="relative z-10 py-10 px-4">

        <div className="max-w-4xl mx-auto">

          {/* HEADER */}
          <div className="text-center mb-10">

            <div className="flex items-center justify-center gap-4 mb-4">

              <div className="bg-sky-500/20 p-4 rounded-2xl border border-sky-400/30 shadow-lg shadow-sky-500/20">

                <Shield className="w-10 h-10 text-sky-300" />

              </div>

              <h1 className="text-5xl font-extrabold bg-gradient-to-r from-sky-300 via-cyan-200 to-blue-400 bg-clip-text text-transparent">

                Phishing URL Detector

              </h1>

            </div>

            <p className="text-gray-200 text-lg">
              AI-powered cybersecurity system to detect phishing and malicious URLs
            </p>

          </div>

          {/* GLASS CARD */}
          <div className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-3xl shadow-2xl p-8">

            {/* INPUT */}
            <label className="text-sm font-medium text-gray-100">
              Enter URL to Analyze
            </label>

            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example.com"
              className="w-full mt-3 p-4 rounded-xl bg-white/10 border border-white/20 text-white placeholder-gray-300 outline-none focus:ring-2 focus:ring-sky-400"
            />

            {/* BUTTONS */}
            <div className="flex gap-3 mt-5">

              <button
                onClick={handleAnalyze}
                className="flex-1 bg-gradient-to-r from-sky-500 to-blue-600 hover:scale-[1.02] transition-all duration-300 text-white py-4 rounded-xl flex items-center justify-center gap-2 font-semibold shadow-lg shadow-sky-500/30"
              >

                {loading ? (
                  <>
                    <Loader2 className="animate-spin w-5 h-5" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" />
                    Analyze URL
                  </>
                )}

              </button>

              {result && (
                <button
                  onClick={handleReset}
                  className="px-6 rounded-xl border border-white/20 bg-white/10 text-white hover:bg-white/20 transition"
                >
                  Reset
                </button>
              )}

            </div>

            {/* RESULT */}
            {result && (

              <div className={`mt-8 p-6 rounded-2xl border backdrop-blur-lg transition-all duration-500 ${
                result.isPhishing
                  ? "bg-red-500/10 border-red-400/30"
                  : "bg-green-500/10 border-green-400/30"
              }`}>

                {/* RESULT HEADER */}
                <div className="flex items-center gap-4 mb-5">

                  {result.isPhishing ? (
                    <AlertTriangle className="w-10 h-10 text-red-400" />
                  ) : (
                    <Shield className="w-10 h-10 text-green-400" />
                  )}

                  <div>

                    <h2 className={`text-3xl font-bold ${
                      result.isPhishing
                        ? "text-red-400"
                        : "text-green-400"
                    }`}>

                      {result.isPhishing
                        ? "⚠️ PHISHING DETECTED"
                        : "✅ LEGITIMATE WEBSITE"}

                    </h2>

                    <p className="text-gray-300 mt-1">
                      Confidence: {result.confidence}% |
                      Risk Score: {result.riskScore}/100
                    </p>

                  </div>

                </div>

                {/* PROGRESS BAR */}
                <div className="w-full h-4 bg-white/10 rounded-full overflow-hidden mb-5">

                  <div
                    className={`h-full transition-all duration-700 ${
                      result.riskScore < 30
                        ? "bg-green-400"
                        : result.riskScore < 60
                        ? "bg-yellow-400"
                        : "bg-red-500"
                    }`}
                    style={{
                      width: `${result.riskScore}%`
                    }}
                  />

                </div>

                {/* ANALYSIS */}
                <div>

                  <h3 className="font-semibold flex items-center gap-2 mb-3 text-white">

                    <Info className="w-4 h-4" />
                    Analysis

                  </h3>

                  <ul className="list-disc ml-6 text-gray-300 space-y-2">

                    {result.reasons.map((r: string, i: number) => (
                      <li key={i}>{r}</li>
                    ))}

                  </ul>

                </div>

              </div>

            )}

            {/* FEATURES */}
            {result && (
              <FeatureDisplay features={result.features} />
            )}

          </div>

          {/* EXAMPLE URLS */}
          <div className="mt-8 backdrop-blur-xl bg-white/10 border border-white/20 rounded-2xl p-5">

            <h3 className="text-lg font-semibold text-cyan-300 mb-4">
              Try Example URLs
            </h3>

            <div className="flex flex-wrap gap-3">

              {[
                "https://google.com",
                "https://github.com",
                "http://192.168.1.1/secure-login",
                "https://paypal-secure-login-verify-account.com",
                "http://free-amazon-gift-card-win-now.xyz"
              ].map((example, index) => (

                <button
                  key={index}
                  onClick={() => setUrl(example)}
                  className="px-4 py-2 rounded-full bg-white/10 border border-white/20 text-sm text-gray-200 hover:bg-cyan-500/20 hover:border-cyan-400 transition-all duration-300"
                >
                  {example}
                </button>

              ))}

            </div>

          </div>

          {/* FOOTER */}
          <div className="mt-8 text-center text-gray-400 text-sm">
            This tool uses Machine Learning to analyze phishing indicators in URLs.
          </div>

        </div>

      </div>

    </div>
  );
}