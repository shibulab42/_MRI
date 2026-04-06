import json
import os
import re

jsonl_path = r'c:/Users/S.Shibukawa/.gemini/antigravity/scratch/rm_researchers20251203.jsonl'
profile_path = r'c:/Users/S.Shibukawa/.gemini/antigravity/scratch/profile.txt'
output_path = r'c:/Users/S.Shibukawa/.gemini/antigravity/scratch/data.js'

# Read profile.txt to extract Lab Members and Awards
def parse_profile_txt(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract Lab Members
    lab_members = {
        "collaborators": [],
        "masters": [],
        "undergraduates": []
    }
    
    # Extract collaborators (hardcoded format to preserve beautiful rendering)
    lab_members["collaborators"] = [
        {
            "name_ja": "吉丸 大輔",
            "name_en": "Daisuke Yoshimaru",
            "affiliation": "Jikei University School of Medicine, Division of Regenerative Medicine<br>Department of Radiology, Tokyo Medical University",
            "url": "https://researchmap.jp/D_maru"
        },
        {
            "name_ja": "臼井 圭介",
            "name_en": "Keisuke Usui",
            "affiliation": "Faculty of Health Science, Department of Radiological Technology, Juntendo University"
        },
        {
            "name_ja": "林 直弥",
            "name_en": "Naoya Hayashi",
            "affiliation": "Department of Radiology, Tokyo Medical University"
        }
    ]
    
    # Extract Master's students
    masters_match = re.search(r"Master's Course\n(.*?)\n\nUndergraduate", content, re.DOTALL)
    if masters_match:
        masters_text = masters_match.group(1).strip()
        for line in masters_text.split('\n'):
            if line.strip():
                lab_members["masters"].append(line.strip())
    
    # Extract Undergraduate students
    undergrad_match = re.search(r'Undergraduate student\n(.*?)\n\nAwards:', content, re.DOTALL)
    if undergrad_match:
        undergrad_text = undergrad_match.group(1).strip()
        for line in undergrad_text.split('\n'):
            if line.strip():
                lab_members["undergraduates"].append(line.strip())
    
    # Extract Awards
    awards = []
    awards_match = re.search(r'Awards:\n(.*?)\n\n\nPublications:', content, re.DOTALL)
    if awards_match:
        awards_text = awards_match.group(1).strip()
        current_award = []
        for line in awards_text.split('\n'):
            line = line.strip()
            if line:
                current_award.append(line)
                if len(current_award) == 2:  # Award has 2 lines: description and recipient
                    awards.append(' '.join(current_award))
                    current_award = []
    
    return lab_members, awards

lab_members, awards = parse_profile_txt(profile_path)

manual_profile = {
    "name": {
        "ja": "渋川 周平",
        "en": "Shuhei Shibukawa",
        "kana": "シブカワ シュウヘイ"
    },
    "affiliations": [
        { "ja": "順天堂大学 診療放射線学科 准教授", "en": "Associate Professor, Department of Radiological Sciences, Juntendo University" },
        { "ja": "東京大学 大学院総合文化研究科 特任助教", "en": "Project Assistant Professor, Graduate School of Arts and Sciences, The University of Tokyo" },
        { "ja": "東京医科大学 放射線医学分野 非常勤講師", "en": "Part-time Lecturer, Department of Radiology, Tokyo Medical University" }
    ],
    "keywords": [
        { "ja": "磁気共鳴画像(MRI)", "en": "Magnetic Resonance Imaging (MRI)" },
        { "ja": "骨格筋イメージング", "en": "Skeletal Muscle Imaging" },
        { "ja": "脳画像解析", "en": "Brain Image Analysis" }
    ],
    "lab_members": lab_members,
    "awards": awards
}

manual_publications = {
    "international_journals": [
        "Yoshimaru D, Ouchi K, Shibukawa S, Ozawa M, Hirabayashi M, Yuzawa A, Tsurugizawa T, Oishi K, Okano HJ. Data-driven schizophrenia subtyping via brain atrophy trajectories and functional connectivity. Transl Psychiatry. 2026 Mar 19;16(1):229. doi: 10.1038/s41398-026-03968-w.",
        "Shibukawa S, Ozawa T, Takabayashi K, Mizuta K, Uchida W, Yamanaka K, Kim J, Yamazaki K, Iwasaki T, Mizuguchi N, Hagiwara A, Nakaya M, Takahashi M, Waki H, Aoki S, Kamagata K. Associations between MR Imaging-derived Metrics under Exercise Load, Wingate Test Results, and Sprint Performance. Magn Reson Med Sci. 2026 Jan 8. doi: 10.2463/mrms.mp.2025-0122.",
        "Muro I, Isoiwa T, Shibukawa S, Usui K, Otsuka Y. Using Deep Learning to Simultaneously Reduce Noise and Motion Artifacts in Brain MR Imaging. Magn Reson Med Sci. 2025 Feb 13. doi: 10.2463/mrms.mp.2024-0098. Epub ahead of print. PMID: 39938896.",
        "Takahashi K, Noda Y, Hondo N, Shibukawa S, Kamagata K, Wada M, Honda S, Homma S, Tsukazaki A, Tsugawa S, Tobari Y, Moriyama S, Taniguchi K, Koike S, Cassidy C, Mimura M, Uchida H, Nakajima S. Abnormal neuritic microstructures in the anterior limb of internal capsules in treatment-resistant depression - A cross-sectional NODDI study. J Psychiatr Res. 2025 Feb 7;183:93-99. doi: 10.1016/j.jpsychires.2025.02.007. Epub ahead of print. PMID: 39954542.",
        "Hasegawa S, Yoshimaru D, Hayashi N, Shibukawa S, Takagi M, Murai H. Analyzing the relationship between specific brain structural changes and the diffusion tensor image analysis along the perivascular space index in idiopathic normal pressure hydrocephalus. J Neurol. 2024 Dec 12;272(1):56. doi: 10.1007/s00415-024-12850-y. PMID: 39666072.",
        "Shibukawa S, Yoshimaru D, Hiyama Y, Ozawa T, Usui K, Goto M, Sakamoto H, Kyogoku S, Daida H. Differential T2* changes in tibialis anterior and soleus: Influence of exercise type and perceived exertion. J Biomech. 2024 Nov 19;177:112437. doi: 10.1016/j.jbiomech.2024.112437. [Epub ahead of print] PubMed PMID: 39579591.",
        "Yoshimaru D, Tsurugizawa T, Hayashi N, Hata J, Shibukawa S, Hagiya K, Oshiro H, Kishi N, Saito K, Okano H, Okano HJ. Relationship between regional volume changes and water diffusion in fixed marmoset brains: an in vivo and ex vivo comparison. Sci Rep. 2024 Nov 6;14(1):26901. doi: 10.1038/s41598-024-78246-0. PubMed PMID: 39505977; PubMed Central PMCID: PMC11541870.",
        "Yoshimaru D, Tsurugizawa T, Hata J, Muta K, Marusaki T, Hayashi N, Shibukawa S, Hagiya K, Okano H, Okano HJ. Similarity and characterization of structural and functional neural connections within species under isoflurane anesthesia in the common marmoset. Neuroimage. 2024 Oct 15;300:120854. doi: 10.1016/j.neuroimage.2024.120854. Epub 2024 Sep 14. PubMed PMID: 39278381.",
        "Tachibana, H., Hoshino, Y., Watanabe, Y., Usui, K., Mizukami, S., Shibukawa, S., ... & Tachibana, R. (2025). Quality assurance of magnetic resonance imaging for a polymer gel dosimeter using a 3D-printed phantom. Radiation Physics and Chemistry, 226, 112196.",
        "Tanaka T, Saito K, Shibukawa S, Yoshimaru D, Osakabe H, Nagakawa Y, Tajima Y. Differentiation Between Abscesses and Unnecessary Intervention Fluid After Pancreas Surgery Using Dual-Energy Computed Tomography. Cureus. 2024 Jun;16(6):e62811. doi: 10.7759/cureus.62811. eCollection 2024 Jun. PubMed PMID: 39036172; PubMed Central PMCID: PMC11260291.",
        "Bessho T, Hayashi T, Shibukawa S, Kourin K, Shouda T. Clinical application of single-shot fast spin-echo sequence for cerebrospinal fluid flow MR imaging. Radiol Phys Technol. 2024 Sep;17(3):782-792. doi: 10.1007/s12194-024-00825-7. Epub 2024 Jul 19. PMID: 39028437.",
        "Konta N, Shibukawa S, Horie T, Niwa T, Obara M, Okazaki T, Kawamura Y, Miyati T. Turbo spin-echo-based enhanced acceleration-selective arterial spin labeling without electrocardiography or peripheral pulse unit triggering and contrast enhancement for lower extremity MRA. Magn Reson Imaging. 2024 Jul;110:43-50. doi: 10.1016/j.mri.2024.04.008. Epub 2024 Apr 9. PMID: 38604346.",
        "Shibukawa S, Kan H, Honda S, Wada M, Tarumi R, Tsugawa S, Tobari Y, Maikusa N, Mimura M, Uchida H, Nakamura Y, Nakajima S, Noda Y, Koike S. Alterations in subcortical magnetic susceptibility and disease-specific relationship with brain volume in major depressive disorder and schizophrenia. Transl Psychiatry. 2024 Mar 26;14(1):164. doi: 10.1038/s41398-024-02862-7. PMID: 38531856; PMCID: PMC10965930.",
        "Katagiri N, Saho T, Shibukawa S, Tanabe S, Yamaguchi T. Predicting interindividual response to theta burst stimulation in the lower limb motor cortex using machine learning. Front Neurosci. 2024 Mar 20;18:1363860. doi: 10.3389/fnins.2024.1363860. PMID: 38572150; PMCID: PMC10987705.Usui K, Muro I, Shibukawa S, Goto M, Ogawa K, Sakano Y, Kyogoku S, Daida H. Evaluation of motion artefact reduction depending on the artefacts' directions in head MRI using conditional generative adversarial networks. Sci Rep. 2023 May 26;13(1):8526. doi: 10.1038/s41598-023-35794-1.",
        "Shibukawa S, Konta N, Niwa T, Miyati T, Yonemochi T, Yoshimaru D, Horie T, Kuroda K, Sorimachi T. Temperature measurement of intracranial cerebrospinal fluid using diffusion tensor imaging after revascularization surgery in Moyamoya disease. Magn Reson Imaging. 2023 Jun;99:1-6. doi: 10.1016/j.mri.2022.12.027.",
        "Sun X, Niwa T, Okazaki T, Kameda S, Shibukawa S, Horie T, Kazama T, Uchiyama A, Hashimoto J. Automatic detection of punctate white matter lesions in infants using deep learning of composite images from two cases. Sci Rep. 2023 Mar 17;13(1):4426. doi: 10.1038/s41598-023-31403-3.",
        "Hayashi T, Yano S, Shibukawa S, Kojima S, Ito T, Oba H, Kondo H, Yamamoto A, Okamoto T. Impact of arm position on vertebral bone marrow proton density fat fraction in chemical-shift-encoded magnetic resonance imaging: a preliminary study. Quant Imaging Med Surg. 2022 Nov;12(11):5263-5270. doi: 10.21037/qims-22-396.",
        "Yoshimaru D, Araki Y, Matsuda C, Shirota N, Tajima Y, Shibukawa S, Murata K, Nickel D, Saito K. Evaluation of liver tumor identification rate of volumetric-interpolated breath-hold images using the compressed sensing method and qualitative evaluation of tumor contrast effect via visual evaluation. Quant Imaging Med Surg. 2022 May;12(5):2649-2657. doi: 10.21037/qims-21-850.",
        "Shibukawa S, Niwa T, Miyati T, Ogino T, Yoshimaru D, Kuroda K. Temperature measurement of intracranial cerebrospinal fluid using second-order motion compensation diffusion tensor imaging. Phys Med Biol. 2021 Dec 16;66(24). doi: 10.1088/1361-6560/ac3fff.",
        "Watanabe S, Shibukawa S, Hayashi T, Tsuruya K, Niwa T. Influence of arm position on proton density fat fraction in the liver using chemical shift-encoded magnetic resonance imaging. Magn Reson Imaging. 2021 Nov;83:133-138. doi: 10.1016/j.mri.2021.08.001.",
        "Shibukawa S, Konta N, Niwa T, Obara M, Akamine Y, Shinozaki N, Okazaki T, Nagafuji Y, Miyati T. Non-enhanced and Non-gated MR Angiography for Robust Visualization of Peripheral Arteries Using Enhanced Acceleration-selective Arterial Spin Labeling (eAccASL). Magn Reson Med Sci. 2021 Sep 1;20(3):312-319. doi: 10.2463/mrms.tn.2019-0172.",
        "Shibukawa S, Saito M, Niwa T, Obara M, Konta N, Hara T, Okazaki T, Nomura T. Optimized enhanced acceleration selective arterial spin labeling (eAccASL) for non-gated and non-enhanced MR angiography of the hands. Magn Reson Imaging. doi: 10.1016/j.mri.2021.01.003. 2021 Jan. (in press)",
        "Shibukawa S, Konta N, Niwa T, Obara M, Akamine Y, Shinozaki N, Okazaki T, Nagafuji Y, Miyati T. Non-enhanced and Non-gated MR Angiography for Robust Visualization of Peripheral Arteries Using Enhanced Acceleration-selective Arterial Spin Labeling (eAccASL). Magn Reson Med Sci. 2020 Jul 13. doi: 10.2463/mrms.tn.2019-0172.",
        "Katoh H, Shibukawa S, Yamaguchi K, Hiyama A, Horie T, Sato M, Watanabe M. A Combination of Magnetic Resonance Imaging Techniques to Localize the Dural Defect in a Case of Superficial Siderosis-A Case Report. Medicines (Basel). 2020 Jun 25;7(6):36. doi: 10.3390/medicines7060036.",
        "Shibukawa S, Niwa T, Ohno N, Miyati T, Muro I, Ogino T, Matsumae M, Imai Y. Optimal strategy for measuring intraventricular temperature using acceleration motion compensation diffusion-weighted imaging. Radiol Phys Technol. 2020 Jun;13(2):136-143. doi: 10.1007/s12194-020-00560-9.",
        "Horie T, Kajihara N, Saito H, Shibukawa S, Obara M, Ogino T, Niwa T, Kuroda K, Matsumae M. Visualization of Cerebrospinal Fluid Motion in the Whole Brain Using Three-dimensional Dynamic Improved Motion-sensitized Driven-equilibrium Steady-state Free Precession. Magn Reson Med Sci. 2020 Mar 18. doi: 10.2463/mrms.tn.2019-0171.",
        "Okazaki T, Niwa T, Suzuki K, Shibukawa S, Imai Y. Age related signal changes of the pituitary stalk on thin-slice magnetic resonance imaging in infants. Brain Dev. 2019;41(4):327-333. doi:10.1016/j.braindev.2018.11.009",
        "Akamine Y, Obara M, Togao O, Shibukawa S, Yoneyama M, Okuaki T, Van Cauteren M. Robust visualization of middle cerebral artery main trunk by enhanced acceleration-selective arterial spin labeling (eAccASL) for intracranial MRA. Magn Reson Med. 2019 May;81(5):3185-3191. doi: 10.1002/mrm.27603.",
        "Nomura T, Niwa T, Ozawa S, Oguma J, Shibukawa S, Imai Y.The Visibility of the Terminal Thoracic Duct Into the Venous System Using MR Thoracic Ductography with Balanced Turbo Field Echo Sequence. Acad Radiol. 2019 Apr;26(4):550-554. doi: 10.1016/j.acra.2018.04.006.",
        "Obara M, Togao O, Beck GM, Shibukawa S, Okuaki T, Yoneyama M, Nakamura M, Honda H, Van Cauteren M. Non-contrast enhanced 4D intracranial MR angiography based on pseudo-continuous arterial spin labeling with the keyhole and view-sharing technique. Magn Reson Med. 2018 Aug;80(2):719-725. doi: 10.1002/mrm.27074.",
        "Niwa T, Yoneda T, Hayashi M, Suzuki K, Shibukawa S, Okazaki T, Imai Y. Characteristic phase distribution in the white matter of infants on phase difference enhanced imaging. J Neuroradiol. 2018 Oct;45(6):374-379. doi: 10.1016/j.neurad.2018.03.001.",
        "Shibukawa S, Miyati T, Niwa T, Matsumae M, Ogino T, Horie T, Imai Y, Muro I.　Time-spatial Labeling Inversion Pulse (Time-SLIP) with Pencil Beam Pulse: A Selective Labeling Technique for Observing Cerebrospinal Fluid Flow Dynamics. Magn Reson Med Sci. 2018 Jul 10;17(3):259-264. doi: 10.2463/mrms.tn.2017-0032.",
        "Nomura T, Niwa T, Koizumi J, Shibukawa S, Ono S, Imai Y. Magnetic resonance thoracic ductography assessment of serial changes in the thoracic duct after the intake of a fatty meal. J Anat. 2018 Mar;232(3):509-514. doi: 10.1111/joa.12761.",
        "Mizuma A, Kouchi M, Shibukawa S, Ikeda S, Ishihara M, Iino M, Yanagimachi N, Nagata E, Takizawa S. High-resolution imaging of complex aortic plaques in ischemic stroke patients using 3.0 Tesla MRI with VISTA. Cardiol J. 2017;24(1):105-106. doi: 10.5603/CJ.2017.0010.",
        "Nomura T, Niwa T, Kazama T, Sekiguchi T, Okazaki T, Shibukawa S, Nishio H, Obara M, Imai Y. Balanced Turbo Field Echo with Extended k-space Sampling: A Fast Technique for the Thoracic Ductography. Magn Reson Med Sci. 2016 Oct 11;15(4):405-410. doi: 10.2463/mrms.tn.2015-0111.",
        "Obara M, Togao O, Yoneyama M, Okuaki T, Shibukawa S, Honda H, Van Cauteren M.　Acceleration-selective arterial spin labeling for intracranial MR angiography with improved visualization of cortical arteries and suppression of cortical veins. Magn Reson Med. 2017 May;77(5):1996-2004. doi: 10.1002/mrm.26275.",
        "Shibukawa S, Nishio H, Niwa T, Obara M, Miyati T, Hara T, Imai Y, Muro I. Optimized 4D time-of-flight MR angiography using saturation pulse. J Magn Reson Imaging. 2016 Jun;43(6):1320-6. doi: 10.1002/jmri.25118.",
        "Mizuma A, Ishikawa T, Kajihara N, Takano H, Endo K, Kawakata M, Shibukawa S, Nakamura T, Nishio H, Horie T, Yanagimachi N, Takizawa S. Dynamic cross-sectional changes of the middle cerebral artery in atherosclerotic stenosis detected by 3·0-Tesla MRI. Neurol Res. 2014 Sep;36(9):795-9. doi: 10.1179/1743132813Y.0000000309."
    ],
    "domestic_journals": [
        "小林明日香, 渋川周平, 高野晋, 室伊三男.　頭部FLAIR 画像におけるpackage 数がコントラストに及ぼす影響，日本放射線技術学会雑誌 74(10), 1180-1185, 2018",
        "今田奈津夫, 渋川周平, 白鳥智章, 堀江朋彦, 小原真．撮像パラメータがSynthetic MRI に及ぼす影響について．日本放射線技術学会雑誌 74(2), 117-123, 2018",
        "高野晋, 堀江朋彦, 遠藤和之, 渋川周平, 本田真俊, 室伊三男, 荻野徹男．呼吸同期を併用した Spectral Attenuated with Inversion Recovery 脂肪抑制法の問題点．日本放射線技術學會雜誌 69(1), 92-98, 2013-01-20",
        "渋川周平，西尾広明，堀江朋彦，室伊三男．Multi transmit における画像均一性とコントラストの基礎的検討，日本放射線技術學會雜誌．2011; 67: 1192-1199."
    ],
    "books": [
        "MR撮像技術学, 日本放射線技術学会, 齋藤, 茂芳, 渋川周平 (担当:分担執筆, 範囲:MR_Hydrography), オーム社 2024年10月 (ISBN: 9784274232626)",
        "室伊三男 (編集), 遠藤和之，梶原直，渋川周平，高野隼，中村智哉，西尾広明，山本和幸（著）, \"現場で役立つMRI読本\", PILAR PRESS, May, 2014"
    ],
    "domestic_conferences": [
        "渋川周平, \"3.0TMRIにおけるアーチファクト\", 第70回日本放射線技術学会総会学術大会.基礎講座, 2014年4月",
        "渋川周平, \"脊椎MRIにおける基礎から応用シークエンスまで\"，第75回日本放射線技術学会総会学術大会.第72回撮影部会"
    ],
    "international_conferences": [
        "Shibukawa S, kan H, Noda Y, Nakajima S, Takabayashi K, Kamagata K, Koike S. Subcortical Analysis in Major Depressive Disorder Using Apparent Fiber Density and Quantitative Susceptibility Mapping. Neuro2024. (Fukuoka Japan)",
        "Shibukawa S, kan H, Noda Y, Nakajima S, Maikusa N, Nakajima S, Koike S. Subcortical morphometry and magnetic susceptibility analysis in major depression disorder. NEURO2022 (Okinawa, Japan)",
        "Shibukaw S, Niwa T, Miyati T, Saito M, Ogino T, Yoshimaru D, Kuroda K. Measurement of intraventricular temperature in the whole brain using second order motion compensation DTI, ISMRM 27th Annual Meeting & Exhibition. (Montreal. Canada.)",
        "Horie　T, Kajihara N, Saito H, Shibukawa S, Takano S, Konta N, Obara M, Ogino T, Niwa T, Kuroda K, Matsumae M, \" Visualization of irregular CSF flow by dynamic iMSDE SSFP using acceleration- selective motion - sensitized gradient (AS-MSG)\", ISMRM 27th Annual Meeting & Exhibition. (Montreal. Canada.)",
        "Konta N, Shibukawa S, Obara M, Akamine Y, Horie T, Okazaki T, Nagafuji Y, Niwa T, Imai Y, \" A comparison of Enhanced Acceleration-Selective Arterial Spin Labeling (eAccASL) and Background Suppressed Single shot TFE-TRANCE (BASS TRANCE) for the peripheral arteries \", ISMRM 27th Annual Meeting & Exhibition. (Montreal. Canada.)",
        "Horie　T, Kajihara N, Saito H, Shibukawa S, Takano S, Konta N, Obara M, Ogino T, Niwa T, Kuroda K, Matsumae M, \"Visualization of CSF flow of whole brain using 3D dynamic iMSDE SSFP\", ISMRM 27th Annual Meeting & Exhibition. (Montreal. Canada.)",
        "Shibukawa S, konta N, Niwa T, Obara M, Miyati T, Imai Y, Iwatsubo T, \"Non-enhanced and non-gated MR angiography for peripheral arteries using improved acceleration-selective arterial spin labelling (iAccASL)\" , Radiological Society of North America 2018. (Chicago. USA.)",
        "Akamine Y, Obara M, Togao O, Shibukawa S, Yoneyama M, Okuaki T, Van Cauteren　M, Chida N, Iwatsubo T, \"Robust　Visualization of MCA Main Trunk by Improved Acceleration-Selective Arterial Spin Labeling (iAccASL) for Intracranial MR Angiography\" , ISMRM 25th Annual Meeting & Exhibition. (Hawaii. USA.)",
        "Takano S, Ogino T, Shibukawa S, Horie T, Muro I, Kajihara N, Saito T, Niwa T, Kazama T, Imai Y, \"A Novel Technique for 4D Time-of-Flight MR Angiography using Double Adiabatic Inversion Recovery Pulses\", ISMRM 25th Annual Meeting & Exhibition. (Hawaii. USA.)",
        "Obara　M, Togao O, Fujima N, Shibukawa S, Yoneyama M, Okuaki T, Nakamura M, Van Cauteren　M, \" Scheme optimization for inflow and outflow visualization in non-contrast enhanced dynamic MRA based on pseudo-continuous arterial spin labeling \", ISMRM 25th Annual Meeting & Exhibition. (Hawaii. USA.)",
        "Horie T, Kajihara N, Shibukawa S, Takano S, Saitou T, Niwa T, Matsumae M, Kuroda K, Obara M, Ogino T, Muro I, \"Improvement of dynamic improved motion-sensitized driven-equilibrium steady-state free precession to visualize the irregular motion of cerebrospinal fluid\", ISMRM 25th Annual Meeting & Exhibition. (Hawaii. USA.)",
        "Nomura T, Niwa T, Shibukawa S, Imai Y, \" Visibility of the draining location of the thoracic duct to the venous system on balanced turbo field echo with extended k-space sampling\", ISMRM 25th Annual Meeting & Exhibition. (Hawaii. USA.)",
        "Shibukawa S, Miyati T, Ohno N, NIWA T, Ogino T, Muro I, Imai Y, \" Optimal strategy for measuring intraventricular temperature using Acceleration motion compensation DWI\", ISMRM 25th Annual Meeting & Exhibition. (Hawaii. USA.)",
        "Nakamura T, Shibukawa S, Sainokami Y, Horie T, Muro I, Hasebe T, Imai Y, Ogino T \"Assessment of fractional anisotropy of heart using ECG gating and second moment nulling pulse\", ISMRM 24th Annual Meeting & Exhibition. (Singapore.)",
        "Niwa T, Yoneda T, Shibukawa S, Kazama T, Takahara T, Imai Y, \" Age-related white matter changes on phase difference enhanced imaging in children\", ISMRM 24th Annual Meeting & Exhibition. (Singapore.)",
        "Obara　M, Togao O, Okuaki T, Shibukawa S, Yoneyama M, Van Cauteren　M, \" Non-contrast enhanced 4D intracranial MR angiography based on pseudo-continuous arterial spin labelling (pCASL) with the keyhole technique\", ISMRM 24th Annual Meeting & Exhibition. (Singapore.)",
        "Shibukawa S, Miyati T, Ohno N, NIWA T, Ogino T, Muro I, Imai Y, \"Acceleration motion compensation DWI for measuring intraventricular temperature.\", ISMRM 24th Annual Meeting & Exhibition. (Singapore.)",
        "Niwa T, Yoneda T, Hara T, Sekiguchi T, Nomura T, Okazaki T, Shibukawa S, Yanagimachi N, Takahara T, Imai Y, \"Phase distribution of white matter using phase difference\", ISMRM 22nd Annual Meeting & Exhibition. (Milano. Italy.)",
        "Shibukawa S, Miyati T, Imai Y, Nishio H, Nakamura T, Ogino T, Muro I, \"Time-SLIP with pencil beam pulse for observing CSF flow dynamics.\", ISMRM 22nd Annual Meeting & Exhibition. (Milano. Italy.)."
    ]
}

data = []
try:
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Error decoding line: {e}")
except Exception as e:
    print(f"Error reading file: {e}")

with open(output_path, 'w', encoding='utf-8') as f:
    f.write("const manualProfile = " + json.dumps(manual_profile, ensure_ascii=False, indent=4) + ";\n\n")
    f.write("const manualPublications = " + json.dumps(manual_publications, ensure_ascii=False, indent=4) + ";\n\n")
    f.write("const researcherData = " + json.dumps(data, ensure_ascii=False, indent=4) + ";\n")

print("data.js regenerated successfully with Lab Members and Awards.")
