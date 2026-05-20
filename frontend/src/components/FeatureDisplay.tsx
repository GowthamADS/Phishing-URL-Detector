import { CheckCircle2, XCircle } from "lucide-react";

export function FeatureDisplay({ features }: any) {

  const featureList = [
    {
      label: "URL Length",
      value: features["URL Length"],
      safe: features["URL Length"] < 75
    },

    {
      label: "Number of Dots",
      value: features["Number of Dots"],
      safe: features["Number of Dots"] <= 3
    },

    {
      label: "HTTPS",
      value: features["HTTPS"],
      safe: features["HTTPS"] === "Yes"
    },

    {
      label: "Contains @",
      value: features["Contains @"],
      safe: features["Contains @"] === "No"
    },

    {
      label: "Contains -",
      value: features["Contains -"],
      safe: features["Contains -"] === "No"
    },

    {
      label: "Domain Length",
      value: features["Domain Length"],
      safe: features["Domain Length"] < 30
    },

    {
      label: "Number of Digits",
      value: features["Number of Digits"],
      safe: features["Number of Digits"] < 5
    },

    {
      label: "Special Characters",
      value: features["Special Characters"],
      safe: features["Special Characters"] < 5
    },

    {
      label: "IP Address",
      value: features["IP Address"],
      safe: features["IP Address"] === "No"
    },

    {
      label: "Subdomains",
      value: features["Subdomains"],
      safe: features["Subdomains"] <= 2
    },

    {
      label: "Suspicious Keywords",
      value: features["Suspicious Keywords"],
      safe: features["Suspicious Keywords"] === 0
    }
  ];

  return (

    <div className="mt-8">

      <h3 className="text-lg font-bold text-white mb-4">
        Extracted Features:
      </h3>

      <div className="grid grid-cols-2 gap-4">

        {featureList.map((feature, index) => (

          <div
            key={index}
            className="bg-white rounded-lg p-4 flex justify-between items-center shadow"
          >

            <span className="text-sm font-medium text-black">
              {feature.label}:
            </span>

            <div className="flex items-center gap-2">

              <span className="font-semibold text-black">
                {String(feature.value)}
              </span>

              {feature.safe ? (

                <CheckCircle2 className="w-5 h-5 text-green-500" />

              ) : (

                <XCircle className="w-5 h-5 text-red-500" />

              )}

            </div>

          </div>

        ))}

      </div>

    </div>
  );
}