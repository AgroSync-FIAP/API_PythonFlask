from serpapi import GoogleSearch

url = 'https://floresdachapada.com.br/wp-content/uploads/2021/04/IMG_7098.jpg'

params = {
  "engine": "google_lens",
  "url": url,
  "hl": "pt-br",
  "api_key": "c46e47c982a98cc02743d388300241e7fd73473687b7ce283d6866ae7ed42489"
}

search = GoogleSearch(params)
results = search.get_dict()
visual_matches = results["visual_matches"]
print(visual_matches)
