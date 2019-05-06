# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 18:56:43 2019

@author: aashaar
"""
from __future__ import unicode_literals
import spacy
from nltk import Tree
import pprint
import pysolr
import json

en_nlp =spacy.load('en_core_web_sm')


"""Function to print dependency parsed trees: """
def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
    else:
        return node.orth_

"""Funtion to get list of PP from a sentences"""
def get_pps(doc):
    "Function to get PPs from a parsed document."
    pps = []
    #verbs = []
    #curr_verb = ""
    for token in doc:
        # Try this with other parts of speech for different subtrees.
        #if token.pos_ == 'VERB' and token.orth_ != curr_verb:
            #curr_verb = token;
        #print(token)
        if token.pos_ == 'ADP':
            pp = ' '.join([tok.orth_ for tok in token.subtree])
            pps.append(pp)
            #verbs.append(curr_verb)
    return pps



result_sent_set=["Abraham Lincoln: A Resource Guide from the Library of Congress\n\"Life Portrait of Abraham Lincoln\", from C-SPAN's American presidents: Life Portraits, June 28, 1999\n\"Writings of Abraham Lincoln\" from C-SPAN's American Writers: A Journey Through History\nAbraham Lincoln: Original Letters and Manuscripts – Shapell Manuscript Foundation\nLincoln/Net: Abraham Lincoln Historical Digitization Project – Northern Illinois University Libraries\nTeaching Abraham Lincoln – National Endowment for the Humanities\nWorks by Abraham Lincoln at Project Gutenberg\nWorks by or about Abraham Lincoln at Internet Archive\nWorks by Abraham Lincoln at LibriVox (public domain audiobooks)\nIn Popular Song:Our Noble Chief Has Passed Away by Cooper/Thomas\nAbraham Lincoln Recollections and Newspaper Articles Collection, McLean County Museum of History\nDigitized items in the Alfred Whital Stern Collection of Lincolniana in the Rare Book and Special Collections Division in the Library of Congress"]
result_sent_set = ["Assassination\nAbraham Lincoln was assassinated by John Wilkes Booth on Good Friday, April 14, 1865, while attending a play at Ford's Theatre, five days after Lee's surrender."]
result_sent_set = ["Assassination\nAbraham Lincoln was assassinated by John Wilkes Booth on Good Friday, April 14, 1865, while attending a play at Ford's Theatre, five days after Lee's surrender.","Apple was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in April 1976 to develop and sell Wozniak's Apple I personal computer.","Abraham Lincoln: A Resource Guide from the Library of Congress\n\"Life Portrait of Abraham Lincoln\", from C-SPAN's American presidents: Life Portraits, June 28, 1999\n\"Writings of Abraham Lincoln\" from C-SPAN's American Writers: A Journey Through History\nAbraham Lincoln: Original Letters and Manuscripts – Shapell Manuscript Foundation\nLincoln/Net: Abraham Lincoln Historical Digitization Project – Northern Illinois University Libraries\nTeaching Abraham Lincoln – National Endowment for the Humanities\nWorks by Abraham Lincoln at Project Gutenberg\nWorks by or about Abraham Lincoln at Internet Archive\nWorks by Abraham Lincoln at LibriVox (public domain audiobooks)\nIn Popular Song:Our Noble Chief Has Passed Away by Cooper/Thomas\nAbraham Lincoln Recollections and Newspaper Articles Collection, McLean County Museum of History\nDigitized items in the Alfred Whital Stern Collection of Lincolniana in the Rare Book and Special Collections Division in the Library of Congress"]
result_PP_set =[]
for s in result_sent_set:
    doc = en_nlp(s)
    [to_nltk_tree(sent.root).pretty_print() for sent in doc.sents]
    result_PP_set.append(get_pps(doc))
    print(get_pps(doc))
 


results = solr.search(q=query,start=0, rows=10000)
    print("length of the results", len(results))
    for result in results:
        #print("The title is '{0}','{1}'.".format(result['sentence'],result['name']))
        print(result['name'])



from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
  
example_sent = "when was Abraham Lincoln killed?"#"When did Warren Buffett buy Berkshire Hathaway's shares?"#"This is a sample sentence, showing off the stop words filtration."
example_sent = example_sent.lower()
stop_words = set(stopwords.words('english'))| set(string.punctuation)


word_tokens = word_tokenize(example_sent) 
  
filtered_sentence = [w for w in word_tokens if not w in stop_words] 
print(filtered_sentence) 
 
  
print(word_tokens) 


query= "entity_labels_list:\"DATE\" AND "
for token in filtered_sentence:
    query += "(word_tokens:\""+token+"\" OR lemmatize_word:\""+token+"\" OR synonymns_list:\""+token+"\" OR hypernyms_list:\""+token+"\" OR meronyms_list:\""+token+"\" OR entites_list:\""+token+"\") AND "
query = query[:-4]


print(query[:-4])

sentence_nlp = word_tokenize("Steve Jobs founded Apple in 1980")

import spacy
#nlp = spacy.load("en_core_web_sm")
doc = nlp("Steve Jobs founded Apple in 1980 and went public in 1933") #("I shot an elephant in my sleep")
#doc =nlp("Apple was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne on 5th March April 1976 to develop and sell Wozniak's Apple I personal computer.")
doc =nlp("The Lincolns' last descendant, great-grandson Robert Todd Lincoln Beckwith, died in 1985.")
for token in doc:
    print("{2}({3}-{6}, {0}-{5})".format(token.text, token.tag_, token.dep_, token.head.text, token.head.tag_, token.i+1, token.head.i+1))
    if(token.text == "Apple"):
        print("*********Verb is--> ", token.head.text)


import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp(u"Autonomous cars shift insurance liability toward manufacturers")
for token in doc:
    print(token.text, token.dep_, token.head.text, token.head.pos_,
            [child for child in token.children])

## *************** Answer to WHEN and WHERE questions ********************
import en_core_web_sm
nlp = en_core_web_sm.load()
term1 = "DATE" #"LOC"
term2 = "TIME"#"GPE"

query = "entity_labels_list:(\"DATE\",\"TIME\" )^10 AND ((word_tokens:apple,go,public)^10 AND (lemmatize_word:apple,go,public) AND (synonymns_list:XTC,cristal,break_down,ecstasy,crack,give_way,pass,break,choke,populace,hold_up,conk,locomote,belong,fail,go_away,buy_the_farm,snuff_it,exit,Malus_pumila,tour,kick_the_bucket,sound,run_low,get,plump,expire,pass_away,depart,whirl,world,rifle,croak,go_game,fling,move,run,live_on,X,endure,pop_off,turn,go_bad,start,cash_in_one's_chips,orchard_apple_tree,conk_out,blend_in,last,survive,give-up_the_ghost,apple,travel,give_out,decease,drop_dead,go,extend,hold_out,hug_drug,lead,die,fit,function,spell,perish,work,blend,public,proceed,get_going,operate,run_short,disco_biscuit,live,Adam,become,offer) AND (hypernyms_list:endeavour,come_about,move,exit,search,select,board_game,get_out,consort,attempt,MDMA,pass_off,false_fruit,duty_period,body,effort,happen,accord,fit,vanish,turn,pass,go_on,terminate,cause_to_be_perceived,shift,finish,harmonise,pick_out,leave,occur,fit_in,pome,methylenedioxymethamphetamine,end,change_state,disappear,stop,act,be,choose,go_away,fall_out,compare,take_place,change,people,harmonize,agree,edible_fruit,work_shift,concord,cease,endeavor,take,hap,apple_tree,try,go_out) AND (hyponyms_list:shuttle,cannonball_along,drag,blare,spirt,arise,shove_off,taxi,splat,embark,bombinate,go_on,break,slice_through,stifle,thud,twang,clangour,continue,jounce,resound,buy_it,seek,sober_up,take_off,pop,speed,wing,fall,accompany,get_off_the_ground,hurtle,clunk,go_deep,swoosh,chatter,serve,rustle,swing,travel_rapidly,run,click,carry,turn,shove_along,come_down,back,billow,snap,burble,fly,birr,snarl,pass_by,bluff_out,drum,blow,stand_up,ramble,go_down,roll,resort,crash,abort,tinkle,get_about,lurch,fare,resonate,circulate,precede,spread,perennate,go_far,crank,rove,drone,step,zip,move_back,babble,pass_on,bucket_along,ferry,transfer,whir,eating_apple,peal,chug,pull_away,beetle,beat,plough,tweet,ease,bounce,ski,swan,weave,range,grumble,tessellate,whistle,rise,whoosh,clangor,get_around,rush,echo,steam,service,angle,ring,pan,ruff,go_across,follow,claxon,pace,noise,be_adrift,prance,circuit,retire,whiz,starve,tink,ping,overfly,move_on,misfunction,beep,lift,live_out,tramp,withdraw,slosh,admass,buzz,forge,steamroller,change,blow_out,retrograde,descend,plow,swish,predecease,advance,surpass,go_around,hurry,crabapple,jump,work,proceed,thrum,make_out,suffocate,stalemate,draw_back,creep,scramble,maneuver,go_up,gurgle,hasten,move_up,trundle,ticktack,vagabond,hotfoot,slice_into,whisk,drown,cut,journey,crack,squelch,snowshoe,round,outflank,thread,pitter-patter,hold_up,stray,trump,thump,push,island_hop,guggle,chime,sober,drift,rumble,come_on,clop,sing,burn_out,drag_out,venture,honk,chink,wheel,swap,wander,twirp,play,progress,famish,pull_back,double,slide,crab_apple,spurt,repair,float,do,ripple,move_around,joint,pink,retreat,hiss,shack,din,splosh,glug,flock,whirr,manoeuvre,go_by,rattle,breeze,travel_along,belt_along,return,betake_oneself,bluff,hold_water,swosh,take_effect,meander,clank,purr,knock,drive,slush,pass_over,malfunction,ride,come,rush_along,ascend,succumb,derail,lap,err,hie,take_the_air,bubble,circle,open,toot,cruise,get_along,misfire,pursue,walk,step_on_it,pass,go_forward,steamer,radiate,glide,bleep,tick,clang,swim,vibrate,settle,precess,draw,take,automobile,zoom,patter,whish,yield,crawl,clink,tap,plunk,zigzag,bombilate,reverberate,sit,motor,tram,ghost,make_noise,propagate,sift,boom,travel_by,ting,clump,uprise,cooking_apple,rap,recede,bang,trail,raft,race,manoeuver,come_up,castle,travel_purposefully,roam,ticktock,swash,dessert_apple,travel,whizz,wend,asphyxiate,lance,steamroll,lead,go_through,skirl,boom_out,ray,whine,pelt_along,career,wind,hum,drag_on,splash,go_past,caravan,cast,slither,operate,pip_out,march_on,tread,check) AND (meronyms_list:apple) AND (holonyms_list:apple,orchard_apple_tree,Malus_pumila))"
query = "entity_labels_list:(\"DATE\",\"TIME\" )^10 AND ((word_tokens:apple,inc.,founded)^10 AND (lemmatize_word:apple,inc.,founded) AND (synonymns_list:found,plant,apple,institute,Malus_pumila,ground,launch,set_up,base,orchard_apple_tree,establish,constitute) AND (hypernyms_list:open_up,initiate,edible_fruit,pome,open,apple_tree,pioneer,false_fruit) AND (hyponyms_list:nominate,build,appoint,dessert_apple,crab_apple,fix,eating_apple,cooking_apple,name,crabapple,constitute) AND (meronyms_list:apple) AND (holonyms_list:apple,orchard_apple_tree,Malus_pumila))"
query= "entity_labels_list:(\"DATE\",\"TIME\" )^10 AND ((word_tokens:gettysburg,address,abraham,lincoln)^10 AND (lemmatize_word:gettysburg,address,abraham,lincoln) AND (synonymns_list:Abraham,direct,President_Abraham_Lincoln,address,reference,call,capital_of_Nebraska,destination,name_and_address,speak,Gettysburg,Battle_of_Gettysburg,speech,deal,come_up_to,Ibrahim,savoir-faire,President_Lincoln,Lincoln,cover,handle,computer_address,treat,accost,turn_to,Abraham_Lincoln,plow) AND (hypernyms_list:label,target,initiate,broach,align,direct,stance,apply,address,come_up,tactfulness,street_sign,domestic_sheep,utilize,tact,aim,utilise,aline,access,place,use,intercommunicate,come,speech,code,delivery,line_up,adjust,employ,direction,manner_of_speaking,instruction,Ovis_aries,speech_act,computer_code,point,communicate,geographic_point,turn_to,geographical_point) AND (hyponyms_list:re-address,lecture,dithyramb,speaking,ask,colloquium,address,call,universal_resource_locator,discuss,discourse,talk_about,recognise,talk,speechmaking,oratory,theologize,instrument,abode,approach,theologise,blaze_away,misdirect,keynote,memorialize,sermon,harangue,argument,business_address,street_address,return_address,misaddress,oral_presentation,recognize,public_lecture,URL,inaugural_address,mailing_address,litany,inaugural,allocution,uniform_resource_locator,parameter,impromptu,memorialise,preaching,public_speaking,greet,residence) AND (meronyms_list:ending,postcode,postal_code,closing,close,introduction,ZIP_code,conclusion,end,body,University_of_Nebraska,ZIP) AND (holonyms_list:Pennsylvania,missive,Nebraska,War_between_the_States,NE,Cornhusker_State,letter,PA,American_Civil_War,Keystone_State,United_States_Civil_War))"
query= "entity_labels_list:(\"DATE\",\"TIME\" )^10 AND ((word_tokens:utd,established)^10 AND (lemmatize_word:utd,established) AND (synonymns_list:found,shew,build,institute,naturalized,launch,established,base,establish,constitute,plant,install,make,ground,give,set_up,accomplished,show,constituted,prove,conventional,lay_down,instal,demonstrate,effected) AND (hypernyms_list:open_up,initiate,create,corroborate,substantiate,make,confirm,open,affirm,sustain,pioneer,support) AND (hyponyms_list:nominate,negate,set,build,appoint,prove,pacify,fix,contradict,stultify,prove_oneself,introduce,mark,name,constitute))"
query= "entity_labels_list:(\"DATE\",\"TIME\" )^10 AND ((word_tokens:warren,buffett,buy,berkshire,hathaway,'s,shares)^10 OR (lemmatize_word:warren,buffett,buy,berkshire,hathaway,'s,share) OR (synonymns_list:part,plowshare,grease_one's_palms,Hathaway,share,contribution,corrupt,rabbit_warren,bargain,deal,purchase,steal,Earl_Warren,ploughshare,parcel,divvy_up,buy,portion,warren,bribe,apportion,partake,Anne_Hathaway,Robert_Penn_Warren,percentage,Warren,partake_in,portion_out,Berkshire) OR (hypernyms_list:allocation,try,stock_certificate,believe,intercommunicate,effort,apportionment,give_out,pay,apportioning,be,communicate,residential_district,allotment,burrow,parceling,assets,endeavor,employ,wedge,get,purchase,use,distribute,overlap,utilize,utilise,residential_area,hand_out,stock,acquire,apply,animal_group,attempt,pass_out,tunnel,community,assignation,parcelling,endeavour) OR (hyponyms_list:sop,interest,take_over,allocation,piece,buy_out,pick_up,cut_in,allowance,cut,dispensation,end,allotment,buy_up,buy_off,impulse-buy,pool,travel_bargain,slice,repurchase,communalize,get,double_up,subscribe,pay_off,split,ration,way,profit_sharing,stake,song,osculate,communalise,take,subscribe_to,partake,take_out,tranche,dole,buy_food,buy_back) OR (meronyms_list:Reading,Eton_College) OR (holonyms_list:stock,net_income,mouldboard_plough,net,England,profit,moldboard_plow,lucre,profits,earnings,net_profit))"
query= "entity_labels_list:(\"DATE\",\"TIME\" )^10 AND ((word_tokens:steve,jobs,die)^10 OR (lemmatize_word:steve,job,die) OR (synonymns_list:cash_in_one's_chips,farm_out,choke,expire,problem,pass_away,fail,perish,give_out,drop_dead,chore,pall,Book_of_Job,go,business,task,kick_the_bucket,buy_the_farm,croak,conk,speculate,Job,job,snuff_it,conk_out,subcontract,dice,pop_off,pass,caper,go_bad,exit,give_way,die,die_out,occupation,break,become_flat,line,decease,break_down,line_of_work,give-up_the_ghost) OR (hypernyms_list:invest,lose_it,cutter,shaping_tool,experience,unfortunate,yearn,cutlery,endure,change,play,product,applications_programme,robbery,cube,yen,disappear,chisel,employ,duty,production,cutting_tool,commit,square_block,application,languish,engage,put,vanish,turn,place,hire,application_program,work,pine,obligation,cut_out,activity,feel,difficulty,responsibility,workplace,cheat,unfortunate_person,suffer,change_state,break_down,snap,go_away,ache,do_work) OR (hyponyms_list:drown,malfunction,calling,career,ball-buster,abort,blow_out,blow,situation,crash,balance-of-payments_problem,go_down,misfire,appointment,treadmill,ball-breaker,stamp,fall,race_problem,spot,berth,buy_it,starve,suffocate,accounting,salt_mine,bull,four-spot,stifle,one-spot,five-spot,catering,yield,billet,place,burn_out,five,predecease,land,work,shitwork,confectionery,post,asphyxiate,scut_work,office,vocation,trade,six,photography,profession,employment,biz,stint,six-spot,game,pip_out,succumb,four,metier,position,craft,famish,misfunction,accountancy,sport,medium,farming)  OR (holonyms_list:Old_Testament,Writings,Hagiographa,Ketubim))"
query= "entity_labels_list:(\"DATE\",\"TIME\" )^10 AND ((word_tokens:exxonmobile,created)^10 OR (lemmatize_word:exxonmobile,created) OR (synonymns_list:make,create,produce) OR (hypernyms_list:appoint,charge,create,make,move,act) OR (hyponyms_list:piece,construct,squeeze_out,burn,form,develop,put_on,cleave,multiply,turn_in,call_down,re-create,institute,suds,initiate,start,write,actualize,customize,father,work,kindle,incorporate,short-circuit,churn_out,underproduce,make_for,remake,beget,recreate,slap_together,bear,cause,carve_out,tailor-make,bootleg,breed,clear,realise,bring_about,custom-make,render,clap_together,extrude,engender,film,redo,fudge_together,do,scrape,put_out,bring_forth,create_from_raw_stuff,pulse,create_verbally,twine,distil,reproduce,elicit,create_from_raw_material,press,conjure,raise,manufacture,film-make,evoke,turn_out,make_over,reinvent,enkindle,set_up,create,regenerate,make,copy,laminate,substantiate,draw,create_by_mental_act,cut,froth,create_mentally,preassemble,distill,confect,educe,customise,extract,arouse,organize,provoke,mother,stir,puncture,clap_up,beat,chop,give,short,compose,actualise,put_forward,give_rise,tack_together,print,establish,smelt,derive,fire,pulsate,choreograph,organise,track,shell,assemble,tack,overproduce,refashion,build,produce,bring,design,play,offset,sire,grind,spume,realize,generate,lay_down,machine,get,elaborate,yield,style,put_together,proof,dummy,call_forth,blast,strike,paint,conjure_up,direct,output,dummy_up,prepare,wreak,procreate,invoke,return,originate,bring_up,throw_together,prefabricate,publish))"

query = "entity_labels_list:(\"GPE\",\"LOC\" ) AND ((word_tokens:apple,open,first,retail,store)^50 AND (lemmatize_word:apple,open,first,retail,store) AND (synonymns_list:fund,loose,open_air,open,first_off,first,out-of-doors,get-go,storage,starting_time,number_1,store,assailable,open_up,foremost,world-class,storehouse,beginning,stack_away,salt_away,exposed,Malus_pumila,undefendable,low,first-class_honours_degree,lay_in,for_the_first_time,first_base,candid,memory_board,spread_out,inaugural,clear,kickoff,entrepot,1st,initiatory,hive_away,start,low_gear,showtime,give,orchard_apple_tree,depot,undecided,surface,capable,receptive,undefended,unfold,unfastened,subject,apple,computer_storage,firstly,shop,initiative,undetermined,heart-to-heart,retail,spread,overt,commencement,outset,put_in,memory,stock,offset,stash_away,opened,first_gear,computer_memory,unresolved,afford,number_one,first_of_all,maiden,outdoors) AND (hypernyms_list:general_knowledge,move,storage_device,honours,exhibit,marketing,memory_device,depository,public_knowledge,arise,come_up,expose,point_in_time,hold_on,false_fruit,gear_mechanism,yield,gear,turn,repository,start,exterior,commence,honours_degree,depositary,give,sales_outlet,deposit,mercantile_establishment,area,rank,ordinal,display,tourney,pome,change_state,country,selling,ordinal_number,retail_store,accumulation,outside,hardware,afford,position,merchandising,undo,point,sell,edible_fruit,keep,computer_hardware,start_up,tournament,outlet,apple_tree,no.,embark_on,go) AND (hyponyms_list:perfumery,tobacco_shop,deli,toyshop,loan_office,chemist's,beauty_salon,military_issue,eating_apple,garage,dress_shop,shoe_shop,hoard,nonvolatile_storage,mens_store,uncork,non-volatile_storage,reposit,novelty_shop,flower_store,former,provision,victual,canteen,virtual_storage,uncross,threshold,railhead,bookstall,loft,bakehouse,birth,chain_store,butcher_shop,bookshop,unbar,confectionery,gift_shop,outfitter,commissary,fixed_storage,hat_shop,virtual_memory,unseal,tobacconist_shop,granary,chemist's_shop,garner,found,powder_magazine,amass,off-licence,dump,incipiency,pharmacy,bin,base,jimmy,accumulate,haberdashery_store,ironmonger's_shop,pizzeria,salon,collect,divaricate,magazine,building_supply_house,double_first,beauty_shop,millinery,pry,liquor_store,pizza_parlor,splay,crab_apple,roll_up,delicatessen,apothecary's_shop,dry_cleaners,terminus_a_quo,shoe-shop,convenience_store,butterfly,haberdashery,treasure_house,food_shop,compile,cooking_apple,computerise,unbolt,stash,unfasten,thriftshop,read-only_memory,ensile,florist_shop,starting_point,pawnbroker's_shop,bakery,incipience,bodega,unlock,specialty_store,mothball,breach,warehouse,meat_market,barbershop,shoe_store,bazar,boutique,pile_up,gap,storage_warehouse,dessert_apple,pawnshop,florist,fix-it_shop,computerize,click_open,repair_shop,inaugurate,bazaar,seed_stock,read-only_storage,prize,clothing_store,lever,ROM,bookstore,prise,infrastructure,second-hand_store,lance,hive,launch,pet_shop,establish,exfoliate,cleaners,package_store,set_up,fly_open,crabapple,hardware_store,building_supply_store,junk_shop,bottle,head_shop,beauty_parlor,ironmonger,grass,tobacconist,computer_store,reopen,betting_shop,confectionary,candy_store,wharf,tank,bakeshop,booth,real_storage,scratchpad,break_open,drugstore,pizza_shop,cache,volatile_storage,keep,call_to_order,powder_store,government_issue,issue,beauty_parlour) AND (meronyms_list:shopfront,apple,storefront,register) AND (holonyms_list:auto,computing_machine,electronic_computer,information_processing_system,apple,computing_device,Malus_pumila,machine,data_processor,computer,car,automobile,orchard_apple_tree,motorcar))"
query = "entity_labels_list:(\"GPE\",\"LOC\" ) AND ((word_tokens:thomas,lincoln,purchase,farms)^50 AND (lemmatize_word:thomas,lincoln,purchase,farm) AND (synonymns_list:President_Abraham_Lincoln,buy,leverage,Seth_Thomas,grow,St._Thomas,capital_of_Nebraska,Lowell_Jackson_Thomas,Dylan_Marlais_Thomas,Dylan_Thomas,purchase,Saint_Thomas,President_Lincoln,raise,Lincoln,Thomas_the_doubting_Apostle,Lowell_Thomas,Norman_Mattoon_Thomas,produce,Norman_Thomas,Thomas,farm,Abraham_Lincoln,doubting_Thomas) AND (hypernyms_list:work,domestic_sheep,workplace,influence,do_work,collect,acquire,acquisition,cultivate,mechanical_phenomenon,take_in,get,Ovis_aries) AND (hyponyms_list:take_over,overproduce,buyback,dairy_farm,impulse-buy,vinery,bargain,buy,subscribe_to,purchasing,subscribe,home-farm,buying,dairy,spread,croft,carry,ranch,stud_farm,buy_back,get,piggery,truck_garden,steal,redemption,truck_farm,take_out,farmplace,sheepwalk,farmstead,vineyard,cattle_ranch,farm-place,grange,pick_up,repurchase,cattle_farm,sheeprun,stock_buyback,buy_food,keep,pig_farm,buy_out,take,buy_up,sewage_farm,chicken_farm) AND (meronyms_list:University_of_Nebraska,farmyard,farmhouse) AND (holonyms_list:Cornhusker_State,Nebraska,NE))"
query = "entity_labels_list:(\"GPE\",\"LOC\" ) AND ((word_tokens:melinda,born)^50 OR (lemmatize_word:melinda,born) OR (synonymns_list:take_over,born,contain,assume,conduct,endure,digest,pay,stick_out,put_up,innate,have,deport,comport,expect,hold,gestate,carry,yield,have_a_bun_in_the_oven,give_birth,Born,support,tolerate,acquit,birth,accept,Max_Born,natural,stand,deliver,wear,brook,turn_out,suffer,bear,abide,behave,stomach) OR (hypernyms_list:countenance,gain,clear,realise,create,make,allow,produce,pull_in,include,let,bring_forth,have,realize,transport,take_in,hold,permit,feature,carry,give_birth,bring_in,move,earn,have_got,birth,deliver,take,bear,act) OR (hyponyms_list:posture,clear,balance,bear_up,conduct,cub,hold_still_for,swallow,pose,piggyback,pay,hold_in,whelp,frogmarch,calve,spin_off,assert,sling,stoop,deport,expect,comport,seed,pig,overbear,farrow,fluster,gestate,pup,face_the_music,carry-the_can,walk_around,retain,carry,poise,have_a_bun_in_the_oven,pay_off,stand_for,litter,acquit,sit_out,accept,lamb,put_forward,twin,drop,fruit,confine,fawn,take_a_joke,kitten,crop,enclose,net,bear,have_young,live_with,behave,foal,take_lying_down,deal) OR (meronyms_list:*) OR (holonyms_list:*))"
query = "entity_labels_list:(\"GPE\",\"LOC\" ) AND ((word_tokens:birth,place,oprah,winfrey)^50 OR (lemmatize_word:birth,place,oprah,winfrey) OR (synonymns_list:blank_space,locate,localize,set,identify,invest,rank,nascency,lay,post,direct,pose,giving_birth,point,birthing,position,have,situation,billet,come_out,plaza,aim,order,send,space,localise,nativity,parentage,nascence,property,home,birth,site,grade,place,berth,range,spot,shoes,office,piazza,commit,station,come_in,target,parturition,give_birth,deliver,seat,topographic_point,put,rate,stead,lieu,bear) OR (hypernyms_list:guess,passage,occupation,family_relationship,approximate,stage,race,send,kinship,present,abode,line_of_work,judge,bring_forth,place,displace,job,spend,set,kickoff,part,position,neighbourhood,assign,showtime,somebody,social_rank,line,space,surface_area,produce,start,geographical_region,office,someone,station,square,offset,knowledge,beginning,locate,geographic_region,direct,post,public_square,point,take_aim,delegate,train,social_status,estimate,vicinity,situation,function,business,evaluate,take,relationship,modification,soul,neck_of_the_woods,item,individual,geographic_area,situate,organic_process,condition,expend,locality,get-go,social_station,person,aim,designate,cognition,change,status,move,commencement,neighborhood,role,noesis,alteration,pass_judgment,order,mortal,run,biological_process,outset,depute,represent,first,area,sing,geographical_area,drop,starting_time,determine,expanse,gauge,rank,residence) OR (hyponyms_list:ground,pig,pool,tell,docket,tie_up,librarianship,put_in,childbed,zone,presidentship,fix,sit,site,secernate,chair,egg_laying,labor,stratum,indent,end,nesting_place,speculate,senatorship,job,rulership,baronetage,recess,poise,stewardship,curacy,mastership,magistrature,overlook,curatorship,grave,renascence,lectureship,marshal,travail,managership,legateship,emirate,upgrade,rear,expect,plum,target,hatchery,legation,stand_up,place_down,throne,locate,tribuneship,put_back,childbearing,priorship,middle,ladle,sanctum,introduce,preceptorship,episcopate,prefecture,protectorship,indenture,margin,mecca,situate,cardinalship,tee_up,wing,sainthood,seigneury,settle,judgeship,hiding_place,chairmanship,live_birth,prioritise,crest,colony,landmark,chieftainship,roll_over,vaginal_birth,jar,lamb,tee,rebirth,precentorship,governorship,chancellorship,right,secretaryship,lean,whelp,back,sow,fawn,distinguish,principalship,lay,commandery,service_area,presidency,wardership,left,center,plant,academicianship,incumbency,sinecure,discipleship,load,judicature,indentation,bed,posthumous_birth,boatyard,arrange,delivery,councilorship,vice-presidency,layer,indention,range_in,sign,seed,coffin,replace,lay_over,generalcy,ship,chieftaincy,heights,buy_into,summit,dispose,prioritize,hot_seat,cradle,tip,space,hatch,bishopry,councillorship,repose,consulship,station,pole_position,severalise,residency,place_upright,thaneship,cram,post,clap,install,insert,intersperse,anomaly,situation,accountantship,moderatorship,misplace,farrow,teachership,vantage,instructorship,downgrade,settle_down,throw,lying-in,reposition,editorship,trench,put_down,set_down,regency,messiahship,attorneyship,chaplainship,rest,polls,superpose,viziership,place_of_birth,junction,home_away_from_home,shelter,showplace,juxtaposition,mislay,generalship,foal,home_from_home,niche,drop,seat,pitch,bucket,front,admiralty,polling_station,stratify,have_a_bun_in_the_oven,childbirth,accouchement,solitude,captainship,target_area,garrison,set_up,sanctuary,magistracy,deposit,lose,public_office,chaplaincy,pup,inclose,fund,bear,juxtapose,position,prepose,ensconce,rectorate,step,marshalship,superimpose,headship,custodianship,imbricate,upend,clerkship,rendezvous,hatching,perch,controllership,internship,posit,rabbinate,pigeonhole,differentiate,trusteeship,snuggle,stop,kitten,cub,laying,home_in,premiership,have_young,legislatorship,reincarnation,tell_apart,lieutenancy,solicitorship,emplace,half-staff,commandership,eldership,tomb,apprenticeship,hole-in-the-wall,underlay,deanery,centre,pastorate,ambassadorship,shelve,shortlist,scour,cadetship,khanate,holy,postposition,twin,brooding,birthplace,inspectorship,nestle,gestate,manhood,pride_of_place,litter,holy_place,peasanthood,carry,glycerolise,butt,thrust,level,deanship,parallelize,associateship,recline,fatherhood,sequence,setting,park,place,puddle,pile,secern,parturiency,calving,incubation,apostleship,mayoralty,instal,set,counselorship,stand,foremanship,zero_in,proconsulship,proconsulate,calve,enclose,confinement,peak,seigniory,labour,directorship,proctorship,rectorship,top,appose,address,stick_in,half-mast,siphon,subordinate,feudal_lordship,bailiffship,barrel,overlordship,high,behalf,treasurership,lie,caliphate,captaincy,sit_down,polling_place,severalize,studentship,separate,prelacy,bottle,cock,rack_up,preposition,reorder,speakership,postpose,viceroyship,primateship,praetorship,pastorship,comptrollership,lead,pillow,farrowing,wardenship,fort,crown,professorship,receivership,prelature,womanhood,superordinate,glycerolize,counsellorship) OR (meronyms_list:*) OR (holonyms_list:lifetime,reproduction,form,life,lifespan,life-time))"

results = None
results = solr.search(q=query,start=0, rows=1)

print("length of the results", len(results))
for result in results:
    #print("The title is '{0}','{1}'.".format(result['sentence'],result['name']))
    doc = nlp(str(result['sentence']))
    answer = ""
    for X in doc.ents:
        if(X.label_ == term1 or X.label_ == term2):
            answer += X.text + ","
            #print("Answer is--> ",X.text)
    #if(answer[:-1].isnumeric()):
    print(answer[:-1])


######################################    
#function to fetch results from SOLR and extract answer from it:
#arguments: 
    #query-> Solr search query formatted to correctly parse in python
    #term1-> Named Entity label of answer
    #term2-> Named Entity label of answer
    #term1 & term2 will always be one of these pairs ('PERSON','ORG'), ('TIME','DATE') & ('GPE','LOC') for WHO, WHEN & WHERE questions respectively.
def getAnswer(query,term1,term2):
    results = None
    results = solr.search(q=query,start=0, rows=1)

    print("length of the results", len(results))
    for result in results:
        #print("The title is '{0}','{1}'.".format(result['sentence'],result['name']))
        doc = nlp(str(result['sentence']))
        answer = ""
        for X in doc.ents:
            if(X.label_ == term1 or X.label_ == term2):
                answer += X.text + ","
            #print("Answer is--> ",X.text)
    #if(answer[:-1].isnumeric()):
        return answer[:-1], result['sentence'], result['name']


##########
#function to create a JSON file:
def createJSONFile():
    data={}
    data['answers'] =[]
    with open('answers.json', 'w') as json_file:  # writing JSON object
        json.dump(data, json_file)

#########
#function to write/append data to the JSON file:  
def writeToJSON(question, answer, sentence, docName):
    #if the JSON file does not exist, create it:
    if(not os.path.isfile('./answers.json')):
        createJSONFile()
    data = {}
    data['answers'] = []
    with open('answers.json') as json_file:  
        data = json.load(json_file)
    data['answers'].append({
            'Question': question,
            'answers': answer,
            'sentences': sentence,
            'documents' : docName            
            })
    with open('answers.json', 'w') as json_file:  # writing JSON object
        json.dump(data, json_file)    
        
#############################################
    
    
    
with open('questions.txt', 'r') as f:
    x = f.readlines()

doc = nlp(sentence)
for X in doc.ents:
    entities.append(X.text)
    entity_labels.append(X.label_)  

"""
Query:
    entities_list:"Abraham Lincoln" AND entity_labels_list: "DATE" AND (word_tokens : 'killed' OR lemmatize_word : 'killed' OR synonymns_list : 'die' OR hypernyms_list : 'die' OR hyponyms_list : 'die' OR meronyms_list : 'die' OR entities_list : 'die')

links:
    https://stackoverflow.com/questions/39100652/python-chunking-others-than-noun-phrases-e-g-prepositional-using-spacy-etc
    https://stackoverflow.com/questions/36610179/how-to-get-the-dependency-tree-with-spacy
    https://www.analyticsvidhya.com/blog/2017/04/natural-language-processing-made-easy-using-spacy-%E2%80%8Bin-python/
    https://universaldependencies.org/u/pos/all.html
    https://spacy.io/usage/linguistic-features

"""    