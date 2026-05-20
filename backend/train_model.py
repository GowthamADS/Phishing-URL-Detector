import os
import pickle
import re
from urllib.parse import urlparse

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def normalize_url(url: str) -> str:
    if "://" not in url:
        return "http://" + url
    return url


def url_features(url: str):
    url = normalize_url(str(url).strip())
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    return [
        len(url),
        url.count('.'),
        1 if url.startswith('https') else 0,
        1 if '@' in url else 0,
        1 if '-' in domain else 0,
        len(domain),
        sum(c.isdigit() for c in url),
        sum(not c.isalnum() for c in url),
        1 if re.match(r"\d+\.\d+\.\d+\.\d+", domain) else 0,
    ]


FEATURE_COLUMNS = [
    'length',
    'dots',
    'https',
    'has_at',
    'has_hyphen',
    'domain_length',
    'num_digits',
    'special_chars',
    'has_ip',
]


def build_synthetic_dataset():
    examples = [
        ('https://google.com', 0),
        ('https://github.com', 0),
        ('https://example.com/login', 0),
        ('https://secure-bank-login.com', 1),
        ('http://192.168.1.1/secure-login', 1),
        ('http://free-amazon-gift-card-win-now-click-here.xyz', 1),
        ('https://paypal-secure-login-verify-account.com', 1),
        ('http://paypal.com', 0),
        ('https://bank.example.com', 0),
        ('http://verify-update-account.net', 1),
        ('https://login.verification-service.io', 1),
        ('https://apple.com', 0),
    ]

    rows = [url_features(url) + [label] for url, label in examples]
    return pd.DataFrame(rows, columns=FEATURE_COLUMNS + ['label'])


def load_dataset(csv_path: str):
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        print('Dataset missing or empty, using fallback synthetic dataset.')
        return build_synthetic_dataset()

    try:
        df = pd.read_csv(csv_path)
    except pd.errors.EmptyDataError:
        print('CSV contains no data, using fallback synthetic dataset.')
        return build_synthetic_dataset()

    if 'url' not in df.columns or 'label' not in df.columns:
        print('CSV missing required columns, using fallback synthetic dataset.')
        return build_synthetic_dataset()

    df = df.dropna(subset=['url', 'label'])
    df = df.drop_duplicates(subset=['url'])
    df['normalized_url'] = df['url'].astype(str).apply(normalize_url)
    df['length'] = df['normalized_url'].apply(len)
    df['dots'] = df['normalized_url'].apply(lambda x: x.count('.'))
    df['https'] = df['normalized_url'].apply(lambda x: 1 if x.startswith('https') else 0)
    df['has_at'] = df['normalized_url'].apply(lambda x: 1 if '@' in x else 0)
    df['has_hyphen'] = df['normalized_url'].apply(lambda x: 1 if '-' in urlparse(x).netloc else 0)
    df['domain_length'] = df['normalized_url'].apply(lambda x: len(urlparse(x).netloc))
    df['num_digits'] = df['normalized_url'].apply(lambda x: sum(c.isdigit() for c in x))
    df['special_chars'] = df['normalized_url'].apply(lambda x: sum(not c.isalnum() for c in x))
    df['has_ip'] = df['normalized_url'].apply(
        lambda x: 1 if re.match(r"\d+\.\d+\.\d+\.\d+", urlparse(x).netloc) else 0
    )

    return df[[*FEATURE_COLUMNS, 'label']]


def main():
    csv_path = 'phishing_url.csv'
    df = load_dataset(csv_path)

    X = df[FEATURE_COLUMNS]
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print('Accuracy:', accuracy_score(y_test, y_pred))

    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)

    print('✅ model.pkl saved')


if __name__ == '__main__':
    main()
