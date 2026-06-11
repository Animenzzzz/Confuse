#!/usr/bin/env python3
"""One-off generator for resource/words.txt and resource/ioswords.txt."""
import re
from pathlib import Path

RESOURCE = Path(__file__).resolve().parent

# OC / system tokens to skip in general word list
RESERVED = {
    "id", "self", "super", "nil", "null", "void", "int", "float", "double",
    "char", "bool", "short", "long", "signed", "unsigned", "const", "static",
    "extern", "register", "volatile", "inline", "typedef", "struct", "union",
    "enum", "class", "protocol", "interface", "implementation", "property",
    "synthesize", "dynamic", "selector", "encode", "end", "import", "include",
    "define", "ifdef", "ifndef", "endif", "pragma", "available", "deprecated",
    "yes", "no", "true", "false", "new", "delete", "sizeof", "return", "break",
    "continue", "switch", "case", "default", "if", "else", "for", "while", "do",
    "goto", "try", "catch", "throw", "finally", "public", "private", "protected",
    "readonly", "nonatomic", "strong", "weak", "copy", "assign", "retain",
    "autorelease", "instancetype", "ibaction", "iboutlet", "iboutletcollection",
    "view", "controller", "delegate", "datasource", "window", "application",
    "object", "string", "array", "dictionary", "number", "data", "date", "url",
    "error", "notification", "block", "dispatch", "queue", "thread", "lock",
    "init", "dealloc", "alloc", "copy", "mutable", "description", "debug",
    "release", "autorelease", "retain", "perform", "responds", "conforms",
    "isEqual", "hash", "class", "superclass", "description", "debugDescription",
}

GENERAL_WORDS = """
alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron
pi rho sigma tau upsilon phi chi psi omega
amber azure birch cedar coral crimson ebony emerald fern garnet hazel ivory jade
kelp lilac maple nacre olive pearl quartz ruby sage teal umber violet willow
acorn anchor atlas beacon bridge canyon cipher compass crest delta drift echo
ember falcon forge glacier harbor horizon island jasper kernel lantern meadow
nebula oracle prism quasar ridge sapphire summit tundra valley zenith
active agile alert ample arctic bold brisk calm clear crisp dense eager faint
gentle grand hardy inner keen light lucid mellow nimble noble plain quiet rapid
sharp sleek solid steady swift tender vivid warm wise young
adapt align apply audit blend build cache chart clamp clear clone craft debug
defer delay embed fetch flush frame grant hover index inject launch merge
mount parse patch pivot probe query queue reset route scale scope shift slice
spawn stack store sweep trace track tweak unify vault watch yield zoom
anchor badge batch blend bloom boost bracket bundle canvas capsule catalog
channel cluster column config context cursor domain entity export fabric
factor filter fixture fragment gateway handle helper holder instance item
journal kernel layout ledger marker matrix module monitor packet panel
pattern payload portal profile record registry render report resource
segment sensor session signal snapshot socket source status stream summary
syntax table target template token tracker trigger utility vector widget
abacus abstract account achieve acquire advance analyze archive arrange assemble
balance barrier battery benefit bracket budget buffer bundle calendar capture
catalog channel circuit cluster collect combine compile compute configure
construct consume contact content context contract convert coordinate
correlate counter craft create credit criteria critical culture currency
current cycle database decimal default deliver density deposit describe
design detail detect device diagram digital dimension direct display distance
distribute document domain dynamic economy element enable engine enhance
ensure entity environment episode estimate evaluate evidence examine exchange
execute expand expert export express extend external extract fabric facility
feature feedback figure filter finance flexible focus format formula fragment
framework function gateway generate generic global gradient graphic gravity
grid group growth handle hardware harvest header heritage horizon identity
impact import improve impulse include increase index indicate industry initial
inline input insight install instance integrate intent interface internal
interval inventory invoice isolate issue journal journey kernel keyword
landscape language launch layer legacy legend license linear linkage liquid
literal locate logical machine maintain manage manual margin marker market
material matrix measure medium member memory merchant message method metric
migrate mineral minimal mirror mission mobile model modern module monitor
motion motive mountain network neutral nominal normal notice numeric objective
observe obtain occupy offset online operate option organic origin output
overall package palette parallel parameter particle partner pattern payment
perform period persist phantom physical pipeline platform portal portion
position positive potential practice precise predict premium prepare present
preserve pressure primary principle priority process produce profile program
project promote prompt proper protect protocol provide publish purchase
quality quantum quarter random range rapid ratio reader reality reason receipt
receive recent record recover reflect region register regular relate release
relevant reliable remain remote render repair replace report request require
reserve resolve resource respond restore result retail retain retrieve return
revenue reverse review rhythm routine sample satellite scenario schedule
science segment select senior sequence service session signal similar simple
simulate single social source spatial special specific spectrum stable
standard station status storage strategy structure student studio subject
submit subscribe substance success summary support surface sustain symbol
system talent target technical template terminal territory texture theory
thermal timeline tolerance traffic transfer transform transit transmit
trigger typical uniform unique universal update upgrade utility validate
variable vehicle version vertical virtual visible visual volume warehouse
warranty weather western workflow
apple apricot banana berry cherry citrus coconut cranberry currant dragonfruit
fig grape grapefruit guava kiwi lemon lime lynx mango melon nectarine orange
papaya peach pear plum pomegranate raspberry strawberry tangerine watermelon
badger beaver bison buffalo camel cheetah coyote dolphin eagle falcon fox
gecko hawk heron jaguar koala leopard lynx moose otter owl panda panther
parrot pelican rabbit raccoon raven shark sparrow tiger turtle walrus whale
wolf zebra ant bee beetle butterfly cicada cricket dragonfly firefly hornet
mantis moth spider wasp worm snail slug crab lobster shrimp squid octopus
coral reef tide wave surf foam spray mist drizzle shower storm blizzard frost
thunder lightning rainbow aurora eclipse comet meteor planet orbit galaxy
nebula quasar pulsar cosmos stellar lunar solar atomic quantum neural digital
binary hex octal pixel vertex shader texture mesh sprite atlas sprite sheet
frame buffer render pass pipeline stage batch instance primitive topology
raster vertex fragment compute kernel driver firmware hardware software
firmware middleware backend frontend fullstack monolith microservice serverless
cloud edge cluster shard replica partition segment bucket shard node pod
daemon service worker cron job task queue event bus message broker topic
publish subscribe broadcast multicast unicast anycast stream batch realtime
latency throughput bandwidth capacity quota limit threshold boundary ceiling
floor baseline benchmark metric counter gauge histogram percentile quantile
sample aggregate rollup drilldown pivot slice dice filter sort rank score
weight bias gradient descent momentum optimizer regularization dropout batchnorm
embedding latent feature tensor matrix vector scalar operand operator operand
compile link load execute interpret bytecode opcode register stack heap
garbage collector allocator pool arena slab cache line page frame segment
syscall interrupt handler trap signal exception fault crash hang deadlock
race condition mutex semaphore condition variable latch barrier spinlock
read write lock shared exclusive optimistic pessimistic transactional
commit rollback savepoint checkpoint snapshot isolation durability atomicity
consistency availability partition tolerance cap theorem eventual strong
weak causal ordered total partial linearizable serializable repeatable
read committed uncommitted phantom dirty stale fresh warm hot cold frozen
archive purge vacuum compact defragment rebalance redistribute migrate
upgrade downgrade patch hotfix rollback forward backward compatible breaking
semver major minor patch prerelease build metadata changelog release note
feature flag toggle switch gate guard rail sandbox staging production
development testing quality assurance acceptance regression smoke sanity
integration endtoend unit functional performance load stress soak spike
chaos resilience failover recovery backup restore disaster business continuity
compliance audit governance policy regulation standard certification accreditation
privacy security encryption decryption cipher plaintext ciphertext hash salt
pepper nonce iv key certificate authority trust chain handshake negotiate
authenticate authorize account role permission scope grant revoke delegate
impersonate federate single signon multifactor biometric password passphrase
pin token session cookie header payload signature verify validate sanitize
escape encode decode serialize deserialize marshal unmarshal flatten nest
unwrap wrap bind unbind attach detach connect disconnect subscribe unsubscribe
listen speak announce whisper shout mute unmute pause resume play stop rewind
forward backward skip seek scan browse scroll paginate infinite lazy eager
prefetch preload postload warmup cooldown throttle debounce bounce coalesce
merge split join union intersect difference complement subset superset
permutation combination factorial power exponent logarithm sine cosine tangent
radian degree minute second millisecond microsecond nanosecond picosecond
frequency amplitude wavelength phase harmonics resonance damping oscillation
equilibrium steady transient impulse step ramp slope intercept correlation
regression classification clustering segmentation detection recognition tracking
prediction forecast estimation interpolation extrapolation smoothing filtering
convolution pooling activation normalization dropout regularization overfit
underfit generalization specialization transfer multitask meta reinforcement
supervised unsupervised semisupervised selfsupervised contrastive generative
discriminative adversarial variational autoencoder transformer attention head
layer block residual skip connection bottleneck expansion contraction dilation
stride padding kernel receptive field anchor proposal region interest bounding
mask keypoint landmark pose gesture emotion sentiment intent entity slot
intent dialogue conversation utterance transcript summary paraphrase translate
tokenize lemmatize stem parse tag chunk dependency syntax semantic pragmatic
ontology taxonomy hierarchy graph tree forest dag mesh hypergraph clique
community modularity centrality betweenness closeness pagerank eigenvector
random walk diffusion propagation infection epidemic cascade viral organic
inorganic synthetic natural artificial manual automatic semiautomatic hybrid
collaborative competitive cooperative adversarial zero sum nonzero pareto
nash equilibrium saddle point optimum local global convex concave linear
nonlinear quadratic cubic polynomial rational exponential logarithmic
trigonometric hyperbolic inverse forward backward central finite difference
gradient jacobian hessian laplacian divergence curl rot gradient flow
hamiltonian lagrangian action energy momentum inertia mass force torque
pressure volume temperature entropy enthalpy Gibbs helmholtz chemical potential
reaction equilibrium kinetics thermodynamics statistical mechanics quantum
relativity spacetime curvature geodesic manifold topology geometry algebra
calculus analysis synthesis deduction induction abduction inference proof
theorem lemma corollary proposition conjecture hypothesis axiom postulate
definition notation convention terminology glossary vocabulary lexicon thesaurus
""".split()

IOS_SUFFIXES = """
View Cell Layer Button Label Field Slider Switch Picker Toolbar TabBar NavBar
Scroll Table Collection Stack Grid Panel Sheet Modal Popup Overlay Badge Chip
Card Tile Banner Header Footer Sidebar Drawer Menu List Row Column Section
Controller Manager Handler Provider Factory Builder Adapter Wrapper Bridge
Coordinator Navigator Presenter Router Gateway Proxy Mediator Observer Listener
Subscriber Publisher Dispatcher Scheduler Executor Worker Agent Broker Facade
Service Repository Store Cache Pool Registry Catalog Index Cataloger Loader
Fetcher Parser Serializer Deserializer Encoder Decoder Formatter Validator
Converter Mapper Transformer Filter Sorter Aggregator Collector Accumulator
Monitor Tracker Recorder Logger Reporter Analyzer Inspector Scanner Probe
Sensor Beacon Signal Emitter Receiver Transmitter Channel Stream Pipeline
Session Context Scope Environment Container Holder Carrier Bundle Package
Payload Resource Asset Catalog Archive Snapshot Backup Restore Checkpoint
Config Settings Preferences Options Profile Policy Rule Constraint Guard
Validator Checker Verifier Auditor Reviewer Editor Composer Assembler Compiler
Renderer Drawer Painter Styler Theme Palette Font Icon Glyph Symbol Marker
Anchor Pin Point Node Vertex Edge Path Route Link Chain Graph Tree Forest
Cluster Group Batch Queue Stack Heap Buffer Channel Pipe Socket Port Endpoint
Interface Protocol Contract Schema Model Entity Record Document Entry Item
Element Component Module Plugin Extension Addon Widget Gadget Instrument
Device Hardware Peripheral Accessory Attachment Accessory Dock Station Hub
Portal Gateway Fence Barrier Gate Valve Switch Valve Lock Latch Hook Clamp
Bracket Mount Frame Shell Envelope Capsule Pod Module Unit Block Chunk Slice
Segment Fragment Particle Molecule Atom Bit Byte Word Token Tag Label Caption
Title Subtitle Heading Footnote Annotation Remark Note Memo Journal Diary Log
Trace Trail Footprint Imprint Stamp Seal Badge Emblem Crest Shield Armor Guard
Sentinel Warden Keeper Steward Curator Custodian Guardian Protector Defender
Champion Advocate Sponsor Patron Mentor Coach Trainer Guide Navigator Pilot
Captain Commander Director Supervisor Overseer Inspector Examiner Evaluator
Assessor Appraiser Estimator Calculator Counter Meter Gauge Dial Scale Ruler
Compass Navigator Mapper Chart Plot Diagram Blueprint Layout Blueprint Sketch
Draft Template Pattern Mold Form Shape Contour Silhouette Outline Border Edge
Margin Padding Inset Offset Gap Spacing Interval Range Span Scope Reach Radius
Diameter Perimeter Area Volume Capacity Weight Mass Density Pressure Force
Energy Power Voltage Current Signal Wave Pulse Rhythm Beat Tick Clock Timer
Alarm Reminder Alert Warning Notice Message Notification Announcement Broadcast
Dispatch Relay Forward Redirect Reroute Reroute Detour Bypass Shortcut Pathway
Corridor Tunnel Channel Duct Vent Shaft Well Spring Source Origin Root Stem
Branch Leaf Flower Fruit Seed Kernel Core Nucleus Center Hub Pivot Axis Pole
Vertex Apex Peak Summit Crest Ridge Plateau Mesa Cliff Bluff Bank Shore Coast
Harbor Port Marina Dock Pier Wharf Terminal Depot Warehouse Storage Vault
Archive Library Gallery Museum Archive Repository Treasury Cache Buffer Pool
Reservoir Tank Cylinder Barrel Crate Box Case Chest Trunk Suitcase Bag Pouch
Pocket Compartment Chamber Room Hall Lobby Foyer Atrium Court Yard Garden
Grove Orchard Vineyard Meadow Prairie Savanna Desert Oasis Lagoon Bay Cove
Inlet Channel Strait Passage Gateway Portal Door Window Gate Entry Exit
Threshold Portal Vestibule Antechamber Alcove Niche Recess Cavity Hollow
Socket Receptacle Slot Groove Channel Trench Ditch Canal Aqueduct Pipeline
Conduit Wire Cable Cord Rope Chain Link Bond Tie Knot Loop Ring Circle
Sphere Globe Orb Disk Plate Panel Board Slate Tablet Screen Display Monitor
Projector Lamp Light Beacon Torch Flare Spark Flame Ember Glow Shine Gleam
Flash Blink Pulse Wave Ripple Surge Rush Flow Stream Current Tide Drift
Breeze Gust Wind Storm Thunder Lightning Rain Snow Frost Ice Crystal Gem
Stone Rock Boulder Pebble Sand Dust Powder Grain Particle Speck Dot Spot
Blot Stain Mark Trace Scar Line Stripe Band Strip Ribbon Tape Strap Belt
Strap Harness Saddle Saddle Pack Bundle Roll Scroll Sheet Page Leaf Folio
Volume Tome Book Manual Guide Handbook Reference Dictionary Lexicon Glossary
Thesaurus Encyclopedia Almanac Atlas Chart Map Plan Scheme Design Blueprint
Layout Framework Scaffold Skeleton Backbone Spine Rib Cage Shell Hull Frame
Chassis Platform Base Foundation Ground Floor Level Tier Stage Phase Step
Stage Scene Act Episode Chapter Part Section Division Segment Fragment Piece
Portion Share Slice Cut Chunk Block Brick Tile Slab Panel Sheet Layer Coat
Film Veil Mask Shield Screen Curtain Drape Blind Shade Filter Lens Prism
Mirror Glass Crystal Lens Focus Zoom Scope Sight View Vision Outlook Prospect
Horizon Skyline Sky Cloud Mist Fog Haze Smoke Steam Vapor Breath Wind Air
Space Zone Region Territory Domain Realm Kingdom Empire State Nation Country
Land Earth Soil Ground Terrain Landscape Scenery Vista Panorama Viewpoint
Outlook Observation Watch Lookout Tower Spire Steeple Pinnacle Peak Summit
Crown Cap Lid Cover Hood Canopy Awning Umbrella Parasol Shade Shelter Refuge
Haven Sanctuary Retreat Lodge Cabin Cottage Hut Shack Shed Barn Stable Pen
Fold Herd Flock Swarm Cluster Colony Hive Nest Den Lair Burrow Cave Grotto
Cavern Chamber Vault Crypt Tomb Grave Pit Well Spring Fountain Source Head
Mouth Lip Rim Edge Brim Border Boundary Limit Frontier Perimeter Outline
Contour Profile Silhouette Shadow Shade Tint Hue Tone Shade Gradient Blend
Mix Fusion Merge Union Alliance Coalition League Guild Order Society Club
Circle Ring Loop Cycle Round Turn Spin Twist Spiral Coil Helix Wave Curve
Arc Bow Bend Flex Stretch Extend Expand Grow Scale Resize Shrink Compress
Compact Condense Concentrate Focus Center Align Adjust Tune Calibrate Balance
Level Square True Straight Direct Clear Plain Simple Basic Core Essential
Primary Main Central Principal Chief Head Lead Front Fore Aft Rear Back Side
Left Right Top Bottom Upper Lower Inner Outer Inner Outer Near Far Close Distant
Local Remote Global Universal General Common Shared Public Private Personal
Custom Special Unique Rare Common Standard Normal Regular Typical Usual
Average Medium Moderate Mild Soft Hard Firm Solid Liquid Gas Plasma Matter
Material Substance Element Compound Mixture Alloy Blend Composite Hybrid
Native Foreign External Internal Inner Outer Upper Lower Higher Lower Greater
Lesser Major Minor Primary Secondary Tertiary Quaternary Final Initial First
Last Next Previous Current Present Past Future Temporal Spatial Logical Physical
Virtual Real Actual Potential Kinetic Static Dynamic Active Passive Positive
Negative Neutral Balanced Stable Unstable Fixed Mobile Portable Stationary
Permanent Temporary Transient Fleeting Lasting Enduring Persistent Constant
Variable Mutable Immutable Readonly Writable Editable Modifiable Adjustable
Configurable Customizable Adaptable Flexible Rigid Strict Loose Tight Firm
Soft Hard Smooth Rough Fine Coarse Sharp Dull Bright Dim Light Dark Clear
Opaque Transparent Translucent Visible Invisible Hidden Secret Open Closed
Locked Unlocked Secure Safe Unsafe Protected Exposed Covered Wrapped Bare
Plain Fancy Simple Complex Easy Hard Difficult Simple Advanced Basic Expert
Novice Beginner Intermediate Advanced Expert Master Professional Amateur
Formal Informal Official Unofficial Legal Illegal Valid Invalid True False
Correct Incorrect Accurate Inaccurate Precise Imprecise Exact Approximate
Rough Smooth Fine Coarse Detailed Summary Brief Short Long Wide Narrow
Broad Thin Thick Deep Shallow High Low Tall Short Big Small Large Tiny Huge
Massive Mini Micro Macro Mega Giga Nano Pico Femto Atto Zepto Yocto Kilo
Milli Centi Deci Deca Hecto Myria
View Controller Manager Delegate DataSource Presenter Navigator Router
Handler Provider Factory Builder Adapter Wrapper Bridge Coordinator Mediator
Observer Listener Subscriber Publisher Dispatcher Scheduler Executor Worker
Service Repository Store Cache Pool Registry Loader Fetcher Parser Serializer
Encoder Decoder Formatter Validator Converter Mapper Transformer Filter Sorter
Monitor Tracker Recorder Logger Reporter Analyzer Inspector Scanner Probe
Renderer Composer Assembler Compiler Interpreter Evaluator Calculator Counter
Helper Utility Tool Kit Set Suite Pack Bundle Module Plugin Extension Addon
Widget Gadget Instrument Device Peripheral Accessory Attachment Dock Station
Portal Gateway Fence Barrier Gate Lock Hook Clamp Bracket Mount Frame Shell
Capsule Pod Unit Block Chunk Slice Segment Fragment Particle Element Component
Model Entity Record Document Entry Item Object Instance Reference Pointer
Link Chain Graph Tree Node Vertex Edge Path Route Map Chart Plot Diagram
Layout Blueprint Template Pattern Mold Form Shape Contour Outline Border
Margin Padding Inset Offset Gap Spacing Interval Range Span Scope Radius
Timer Clock Alarm Reminder Alert Warning Notice Message Notification
Dispatch Relay Forward Redirect Bypass Shortcut Pathway Corridor Tunnel
Channel Duct Pipeline Conduit Wire Cable Cord Rope Bond Tie Knot Loop Ring
Panel Board Slate Tablet Screen Display Monitor Projector Lamp Light Beacon
Button Label Field Switch Slider Picker Toolbar TabBar NavBar Scroll Table
Collection Stack Grid Sheet Modal Popup Overlay Badge Chip Card Tile Banner
Header Footer Sidebar Drawer Menu List Row Column Section Layer Cell
""".split()

# Rare full UIKit/Foundation type names — keep common suffixes like View/Controller
IOS_AVOID = {
    "NSObject", "NSString", "NSArray", "NSDictionary", "NSNumber", "NSData",
    "NSDate", "NSURL", "NSError", "NSNotification", "NSIndexPath", "NSRange",
    "UIView", "UIViewController", "UIApplication", "UIWindow", "UIScreen",
    "UITableView", "UICollectionView", "UINavigationController", "UITabBarController",
    "IBAction", "IBOutlet", "instancetype",
}


def valid_identifier(word: str) -> bool:
    return bool(re.match(r"^[A-Za-z][A-Za-z0-9]*$", word))


def normalize_words(raw_words, lowercase=False, avoid=None):
    avoid = avoid or set()
    seen = set()
    result = []
    for w in raw_words:
        w = w.strip()
        if not w:
            continue
        if lowercase:
            w = w[0].lower() + w[1:] if len(w) > 1 else w.lower()
        if not valid_identifier(w):
            continue
        key = w.lower()
        if key in RESERVED or key in {a.lower() for a in avoid}:
            continue
        if key in seen:
            continue
        seen.add(key)
        result.append(w)
    return result


def write_wordlist(path: Path, words: list[str]):
    path.write_text("\n".join(words) + "\n", encoding="utf-8")


def main():
    general = normalize_words(GENERAL_WORDS, lowercase=True)
    ios = normalize_words(IOS_SUFFIXES, lowercase=False, avoid=IOS_AVOID)

    write_wordlist(RESOURCE / "words.txt", general)
    write_wordlist(RESOURCE / "ioswords.txt", ios)

    print(f"words.txt: {len(general)} words")
    print(f"ioswords.txt: {len(ios)} words")
    print("words sample:", " ".join(general[:8]))
    print("ios sample:", " ".join(ios[:8]))


if __name__ == "__main__":
    main()
