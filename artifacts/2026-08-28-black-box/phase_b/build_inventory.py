"""Derive a public-doc inventory and PRE-EXECUTION coverage matrix."""
import csv
import datetime as dt
from html.parser import HTMLParser
import json
from pathlib import Path

root = Path(__file__).parent
pages = {row['name']: row for row in json.loads((root/'public_docs/manifest.json').read_text())}
inventory = {
    'created_at': dt.datetime.now(dt.timezone.utc).isoformat(),
    'method': 'Direct current public HTML; no package/source inspection. Documented presence is not runtime verification.',
    'scope_limit': 'Library catalog and complete documented verbs namespace; selected public helpers and concepts. Not an exhaustive inventory of every package export.',
    'nouns': [], 'sources': [], 'noun_source_pairs': [], 'verb_namespace': [], 'other_public_surface': [],
}
for table in pages['nouns']['tables']:
    for name, meaning, flavors, coverage in table[1:]:
        sources = flavors.split(', ')
        inventory['nouns'].append({'name':name,'sources':sources,'documented_status':'listed; source-specific support varies',
            'discovered_at':pages['nouns']['url'], 'runtime_verified':False})
        for flavor in sources:
            inventory['noun_source_pairs'].append({'noun':name,'source':flavor,'discovered_at':pages['nouns']['url'],'runtime_verified':False})
for name, provider, nouns in pages['sources']['tables'][0][1:]:
    inventory['sources'].append({'name':name,'nouns':nouns.split(', '),'status':'documented source flavor; certification not independently verified',
        'discovered_at':pages['sources']['url'],'runtime_verified':False})
inventory['sources'].append({'name':'daymet','nouns':[],'status':'candidate; not promoted; not included in supported-source counts',
    'discovered_at':pages['sources']['url'],'runtime_verified':False})
for name, kind, availability, meaning in pages['callables']['tables'][0][1:]:
    inventory['verb_namespace'].append({'name':name,'callable_type':kind,'documented_status':availability,
        'discovered_at':pages['callables']['url'],'runtime_verified':False})
for name, category, page in [
    ('pipe','composition','pipe'),('Verb','composition','pipe'),('Pipe.unwrap','result extraction','pipe'),
    ('Pipe.explain','inspection','pipe'),('lazy object preservation','lazy behavior','pipe'),
    ('project loader returning xarray','custom noun','custom_nouns'),
    ('factory returning callable','custom verb','custom_verbs'),('v.apply','custom verb','custom_verbs'),
    ('source identity and serving revisions','provenance','data'),('list_sources','discovery','data'),
    ('sources','discovery','data'),('describe','discovery','data')]:
    inventory['other_public_surface'].append({'name':name,'category':category,'discovered_at':pages[page]['url'],'runtime_verified':False})
(root/'public_surface.json').write_text(json.dumps(inventory,indent=2)+'\n')

rows=[]
def add(category,item,status='not_attempted',checks='',why='CubeDynamics unavailable after Phase A installation attempt'):
    rows.append({'category':category,'item':item,'planned_checks':checks,'status':status,'attempted':False,'successful':False,
                 'operation_ids':'','blocker':why})
for item in inventory['nouns']:
    add('noun',item['name'],checks='create; dimensions; coordinates; units; attributes; source identity; provenance; plot; transform')
for item in inventory['noun_source_pairs']:
    add('noun_source',item['noun']+'/'+item['source'],checks='small valid retrieval; source identity; available-source comparison')
add('source_candidate','daymet',status='excluded_candidate',why='Explicitly not promoted in public source index')
for item in inventory['verb_namespace']:
    status='excluded_placeholder' if item['documented_status']=='placeholder' else 'not_attempted'
    add('verb' if item['callable_type']=='Grammar verb / pipe stage' else 'helper_or_reserved',item['name'],status,
        'valid call; edge; plausible misuse; composition; dimensions; coordinates; metadata; provenance')
for item in inventory['other_public_surface']:
    add('public_surface',item['name'],checks=item['category'])
for item in ['one/two/three-plus stages','reversed operation order','reduction then transformation','spatial plus temporal',
             'transformation then visualization','intermediate reuse','long-pipeline provenance','lazy materialization',
             'custom noun with built-in verb','built-in noun with custom verb','custom noun with custom verb',
             'NaN/empty/single-cell inputs','misspelled dimension/invalid source/argument','invalid return type',
             'fixed-seed plausible randomized sequences']:
    add('scenario',item)
for number,question in enumerate([
    'How does daily maximum temperature vary across a small Boulder-area grid?',
    'How does the temporal-mean temperature differ between gridMET and PRISM?',
    'Are high-temperature days spatially coincident with high vapor-pressure deficit?',
    'How sensitive is a hot-spell duration summary to the chosen threshold?',
    'Does averaging over space before anomaly calculation change the interpretation?',
    'How does a seasonal precipitation total vary between two nearby areas?',
    'Does an NDVI change coincide with a hot and dry interval?',
    'Can a user-defined temperature conversion preserve coordinates and units?',
    'How do short discharge events vary in timing within one station record?',
    'Can a user bring a local environmental cube through the same analysis pipeline?',
],1):
    add('proposed_scientific_question',f'Q-{number:02}: {question}',checks='Formulate and execute only after an external artifact is available')
for name,goal in [('B-001','wheel-only installation including prereleases'),('B-002','public pip index discovery'),
                  ('B-003','public PyPI metadata with connectivity control and GitHub release assets'),
                  ('B-004','installed distribution metadata and import smoke check')]:
    add('environment_probe',name,status='planned',checks=goal,why='')
with (root/'coverage_plan.csv').open('w',newline='') as stream:
    writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
counts={'nouns':len(inventory['nouns']),'catalog_source_flavors':len(inventory['sources'])-1,
    'noun_source_pairs':len(inventory['noun_source_pairs']), 'verb_namespace_entries':len(inventory['verb_namespace']),
    'implemented_grammar_verbs':sum(i['callable_type']=='Grammar verb / pipe stage' and i['documented_status']=='implemented' for i in inventory['verb_namespace']),
    'compatibility_grammar_verbs':sum(i['documented_status']=='compatibility' for i in inventory['verb_namespace']),
    'implemented_direct_helpers':sum('helper' in i['callable_type'] and i['documented_status']=='implemented' for i in inventory['verb_namespace']),
    'reserved_placeholders':sum(i['documented_status']=='placeholder' for i in inventory['verb_namespace'])}
print(json.dumps(counts,indent=2))
(root/'inventory_counts.json').write_text(json.dumps(counts,indent=2)+'\n')
