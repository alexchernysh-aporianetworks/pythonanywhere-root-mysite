from django.urls import path
from . import views
from .views import kill_task_view

urlpatterns = [

################### pages


    path('', views.run_scripts_page, name='run_scripts_page'),
    path('run_scripts_page/', views.run_scripts_page, name='run_scripts_page'),
    path('amit_scripts/', views.amit_scripts_page, name='amit_scripts_page'),
    path('mediago/', views.mediago_page, name='mediago_page'),
    path('outbrain/', views.outbrain_page, name='outbrain_page'),
    path('zemanta/', views.zemanta_page, name='zemanta_page'),
    path('taboola/', views.taboola_page, name='taboola_page'),
    path('poppin/', views.poppin_page, name='poppin_page'),
    path('maximizer/', views.maximizer_page, name='maximizer_page'),
    path('google/', views.google_page, name='google_page'),
    path('facebook/', views.facebook_page, name='facebook_page'),
    path('twitter/', views.twitter_page, name='twitter_page'),
    path('newsbreak/', views.newsbreak_page, name='newsbreak_page'),
    path('creative/', views.creative_page, name='creative_page'),
    path('tiktok/', views.tiktok_page, name='tiktok_page'),
    path('amir/', views.amir_page, name='amir_page'),
    path('duplicator/', views.duplicator_page, name='duplicator_page'),
    path('sharon/', views.sharon_page, name='sharon_page'),
    path('mgid/', views.mgid_page, name='mgid_page'),
    path('sasha/', views.sasha_page, name='sasha_page'),
    path('rss_articles_db/', views.rss_articles_db_page, name='rss_articles_db_page'),
    path('gpt_executor/', views.gpt_executor_page, name='gpt_executor_page'),
    path('karmel_reports/', views.karmel_reports_page, name='karmel_reports_page'),  # Karmel's reports page
    path('running-tasks/', views.running_tasks, name='running_tasks'),
    path('script-logs/', views.script_logs_page, name='script_logs_page'),
    path('media_buyers_scripts/', views.media_buyers_scripts, name='media_buyers_scripts'),




################### running-tasks page

    path('stop_task/<uuid:unique_code>/', views.stop_task, name='stop_task'),
    path('run_script/<path:script_path>/', views.execute_script, name='execute_script'),
    path('task-status/<int:task_id>/', views.task_status, name='task_status'),
    path('list_scheduled_tasks/', views.list_scheduled_tasks, name='list_scheduled_tasks'),  # Dynamic tasks view
    path('scheduled-tasks/add/', views.add_scheduled_task, name='add_scheduled_task'),
    path('scheduled-tasks/edit/<int:task_id>/', views.edit_scheduled_task, name='edit_scheduled_task'),
    path('scheduled-tasks/delete/<int:task_id>/', views.delete_scheduled_task, name='delete_scheduled_task'),
    path('Kill_Task_page/', views.Kill_Task_page, name='Kill_Task_page'),
    path("kill-task/", kill_task_view, name="kill_task"),


################### Amit page

    path('run-newtabyes3/', views.run_newtabyes3_script, name='run_newtabyes3_script'),
    path('run-backupmaintonic/', views.run_backupmaintonic_script, name='run_backupmaintonic_script'),
    path('run-obyesforreport/', views.run_obyesforreport_script, name='run_obyesforreport_script'),
    path('run_topofferskeywordstonicnew2025_script/', views.run_topofferskeywordstonicnew2025_script, name='run_topofferskeywordstonicnew2025_script'),
    path('run_tonicrsocchannelscreator_script/', views.run_tonicrsocchannelscreator_script, name='run_tonicrsocchannelscreator_script'),
    path('run_tonicrsocchannelspixels_script/', views.run_tonicrsocchannelspixels_script, name='run_tonicrsocchannelspixels_script'),
    path('run_inuvoyesallyesterdaydata2025_script/', views.run_inuvoyesallyesterdaydata2025_script, name='run_inuvoyesallyesterdaydata2025_script'),
    path('run_palaceupdate_script/', views.run_palaceupdate_script, name='run_palaceupdate_script'),
    path('run_Run_SistersDB_script/', views.run_Run_SistersDB_script, name='run_Run_SistersDB_script'),
    path('run_compliance_siteids_script/', views.run_compliance_siteids_script, name='run_compliance_siteids_script'),
    path('run_sisterscompliancepj_script/', views.run_sisterscompliancepj_script, name='run_sisterscompliancepj_script'),
    path('run_systemnewreport_mobile_script/', views.run_systemnewreport_mobile_script, name='run_systemnewreport_mobile_script'),
    path('run_getkeywordsdata_script/', views.run_getkeywordsdata_script, name='run_getkeywordsdata_script'),
    path('run_Main_N2S_Today_script/', views.run_Main_N2S_Today_script, name='run_Main_N2S_Today_script'),



    path('run_obyesforreport_final_script/', views.run_obyesforreport_final_script, name='run_obyesforreport_final_script'),
    path('run_backupmaintonic_final_script/', views.run_backupmaintonic_final_script, name='run_backupmaintonic_final_script'),
    path('run_newtabyes_final_script/', views.run_newtabyes_final_script, name='run_newtabyes_final_script'),
    path('run_trafficclubyesdata_script/', views.run_trafficclubyesdata_script, name='run_trafficclubyesdata_script'),
    path('run_tcyes_2Days_script/', views.run_tcyes_2Days_script, name='run_tcyes_2Days_script'),

    # Creatives Scripts

    path('run_allfbcreatives_script/', views.run_allfbcreatives_script, name='run_allfbcreatives_script'),
    path('run_allcreativestab_script/', views.run_allcreativestab_script, name='run_allcreativestab_script'),
    path('run_allobcreatives_script/', views.run_allobcreatives_script, name='run_allobcreatives_script'),
    path('run_allmediagocreatives_script/', views.run_allmediagocreatives_script, name='run_allmediagocreatives_script'),
    path('run_zemantacreativesall_script/', views.run_zemantacreativesall_script, name='run_zemantacreativesall_script'),
    path('run_poppincreatives_script/', views.run_poppincreatives_script, name='run_poppincreatives_script'),


    # WTHIW Scripts

    path('run_WTHIW_script/', views.run_WTHIW_script, name='run_WTHIW_script'),
    path('run_WTHIW_Copysheets_script/', views.run_WTHIW_Copysheets_script, name='run_WTHIW_Copysheets_script'),


    # Policy Scripts

    path('run_newpolicycheckforall_running_script/', views.run_newpolicycheckforall_running_script, name='run_newpolicycheckforall_running_script'),
    path('run_gen_newpolicycheckforall_script/', views.run_gen_newpolicycheckforall_script, name='run_gen_newpolicycheckforall_script'),

    # Oz

    path('run_copyarticlesdata_script/', views.run_copyarticlesdata_script, name='run_copyarticlesdata_script'),
    path('run_copyarticlesdataexcs_script/', views.run_copyarticlesdataexcs_script, name='run_copyarticlesdataexcs_script'),


    # Karmel tests

    path('run_tcyes_history_script/', views.run_tcyes_history_script, name='run_tcyes_history_script'),
    path('run_dailyfb_test_2_script/', views.run_dailyfb_test_2_script, name='run_dailyfb_test_2_script'),


################### Zemanta page

    path('run_toniczemanta_2_script/', views.run_toniczemanta_2_script, name='run_toniczemanta_2_script'),
    path('run_toniczemanta2_2_script/', views.run_toniczemanta2_2_script, name='run_toniczemanta2_2_script'),
    path('run_zemantayes_script/', views.run_zemantayes_script, name='run_zemantayes_script'),
    path('run_zemanta2D_script/', views.run_zemanta2D_script, name='run_zemanta2D_script'),
    path('run_invuozemantayes_script/', views.run_invuozemantayes_script, name='run_invuozemantayes_script'),
    path('run_zemantainuvoleads_script/', views.run_zemantainuvoleads_script, name='run_zemantainuvoleads_script'),


    path('run_imagescutob_zemanta_script/', views.run_imagescutob_zemanta_script, name='run_imagescutob_zemanta_script'),
    path('run_newuploader_imagescutob_zemanta_script/', views.run_newuploader_imagescutob_zemanta_script, name='run_newuploader_imagescutob_zemanta_script'),


    path('run_zemanta3finals_andrea/', views.run_zemanta3finals_andrea, name='run_zemanta3finals_andrea'),
    path('run_zemanta3finals_tonic_andrea/', views.run_zemanta3finals_tonic_andrea, name='run_zemanta3finals_tonic_andrea'),
    path('run_zemantacreatives7days_andrea_script/', views.run_zemantacreatives7days_andrea_script, name='run_zemantacreatives7days_andrea_script'),


    path('run_zemantaNeedToArchive_script/', views.run_zemantaNeedToArchive_script, name='run_zemantaNeedToArchive_script'),
    path('run_zemantaarchived_1_script/', views.run_zemantaarchived_1_script, name='run_zemantaarchived_1_script'),
    path('run_zemantadataforupload_script/', views.run_zemantadataforupload_script, name='run_zemantadataforupload_script'),
    path('run_Zemanta_L14_script/', views.run_Zemanta_L14_script, name='run_Zemanta_L14_script'),
    path('run_zemanta_whitelists_script/', views.run_zemanta_whitelists_script, name='run_zemanta_whitelists_script'),


    path('run_zemanta_publishers_merged_script/', views.run_zemanta_publishers_merged_script, name='run_zemanta_publishers_merged_script'),
    path('run_publishers_opt_BLACKLISTED_script/', views.run_publishers_opt_BLACKLISTED_script, name='run_publishers_opt_BLACKLISTED_script'),
    path('run_publishers_opt_ENABLED_script/', views.run_publishers_opt_ENABLED_script, name='run_publishers_opt_ENABLED_script'),
    path('run_zemanta_publishers_merged_SOURCES_EXP_script/', views.run_zemanta_publishers_merged_SOURCES_EXP_script, name='run_zemanta_publishers_merged_SOURCES_EXP_script'),


    path('run_zemantaccmps05112024_CcmpsOB_script/', views.run_zemantaccmps05112024_CcmpsOB_script, name='run_zemantaccmps05112024_CcmpsOB_script'),
    path('run_zemantaccmps05112024_CcmpsOB2_script/', views.run_zemantaccmps05112024_CcmpsOB2_script, name='run_zemantaccmps05112024_CcmpsOB2_script'),
    path('run_zemantaccmps05112024_Ccmps_script/', views.run_zemantaccmps05112024_Ccmps_script, name='run_zemantaccmps05112024_Ccmps_script'),
    path('run_zemantaccmps05112024_CcmpsM_script/', views.run_zemantaccmps05112024_CcmpsM_script, name='run_zemantaccmps05112024_CcmpsM_script'),


    path('run_zemantacads_Cadg_script/', views.run_zemantacads_Cadg_script, name='run_zemantacads_Cadg_script'),
    path('run_zemantacadg05112024_Cadg_script/', views.run_zemantacadg05112024_Cadg_script, name='run_zemantacadg05112024_Cadg_script'),
    path('run_zemantaopt_update_script/', views.run_zemantaopt_update_script, name='run_zemantaopt_update_script'), #


    path('run_zemantacads_Cadg2_script/', views.run_zemantacads_Cadg2_script, name='run_zemantacads_Cadg2_script'),
    path('run_zemantacadg05112024_Cadg2_script/', views.run_zemantacadg05112024_Cadg2_script, name='run_zemantacadg05112024_Cadg2_script'),
    path('run_zemantaopt_update2_script/', views.run_zemantaopt_update2_script, name='run_zemantaopt_update2_script'), #
    path('run_zemantaopt_update3_script/', views.run_zemantaopt_update3_script, name='run_zemantaopt_update3_script'), #
    path('run_zemantaopt_update4_script/', views.run_zemantaopt_update4_script, name='run_zemantaopt_update4_script'), #


    path('run_zemantaopt_script/', views.run_zemantaopt_script, name='run_zemantaopt_script'),


################### Taboola page



    path('run_wandkeywords_script/', views.run_wandkeywords_script, name='run_wandkeywords_script'),
    path('run_SYSTEM_report_script/', views.run_SYSTEM_report_script, name='run_SYSTEM_report_script'),
    path('run_all_taboola_budgets_bids_script/', views.run_all_taboola_budgets_bids_script, name='run_all_taboola_budgets_bids_script'),
    path('run_all_taboola_ids_script/', views.run_all_taboola_ids_script, name='run_all_taboola_ids_script'),
    path('run_autogpt_tabooladesc_script/', views.run_autogpt_tabooladesc_script, name='run_autogpt_tabooladesc_script'),
    path('run_morning_script/', views.run_morning_script, name='run_morning_script'),
    path('run_newtabyes_max_script/', views.run_newtabyes_max_script, name='run_newtabyes_max_script'),
    path('run_newtabyess1_script/', views.run_newtabyess1_script, name='run_newtabyess1_script'),
    path('run_tabautooptcr_script/', views.run_tabautooptcr_script, name='run_tabautooptcr_script'),


    path('run_tabcreatives3_script/', views.run_tabcreatives3_script, name='run_tabcreatives3_script'),
    path('run_tabcreatives4_script/', views.run_tabcreatives4_script, name='run_tabcreatives4_script'),
    path('run_tabcreatives2_script/', views.run_tabcreatives2_script, name='run_tabcreatives2_script'),


    path('run_tabcreativesforall_script/', views.run_tabcreativesforall_script, name='run_tabcreativesforall_script'),
    path('run_tabooladatabreakdown_script/', views.run_tabooladatabreakdown_script, name='run_tabooladatabreakdown_script'),
    path('run_tabupdatemaxcpcbid_auto_script/', views.run_tabupdatemaxcpcbid_auto_script, name='run_tabupdatemaxcpcbid_auto_script'),
    path('run_tonicdavid_script/', views.run_tonicdavid_script, name='run_tonicdavid_script'),
    path('run_tabsitescr_script/', views.run_tabsitescr_script, name='run_tabsitescr_script'),
    path('run_newtabyess1_new_script/', views.run_newtabyess1_new_script, name='run_newtabyess1_new_script'),
    path('run_taboola_allaccounts_script/', views.run_taboola_allaccounts_script, name='run_taboola_allaccounts_script'),
    path('run_systemnewreport_script/', views.run_systemnewreport_script, name='run_systemnewreport_script'),
    path('run_tabupdatemaxcpcbid_script/', views.run_tabupdatemaxcpcbid_script, name='run_tabupdatemaxcpcbid_script'),
    path('run_maxcpaandcpcbidstaboolaopt_script/', views.run_maxcpaandcpcbidstaboolaopt_script, name='run_maxcpaandcpcbidstaboolaopt_script'),
    path('run_pausetaboolal7nospend_script/', views.run_pausetaboolal7nospend_script, name='run_pausetaboolal7nospend_script'),
    path('run_tabopt2026_script/', views.run_tabopt2026_script, name='run_tabopt2026_script'),
    path('run_tabopt_status_script/', views.run_tabopt_status_script, name='run_tabopt_status_script'),


    # Taboola page - Wanduum

    path('run_T2tonicrsocwanduumnew3finals_script/', views.run_T2tonicrsocwanduumnew3finals_script, name='run_T2tonicrsocwanduumnew3finals_script'),
    path('run_T3wandrsoccreatives_script/', views.run_T3wandrsoccreatives_script, name='run_T3wandrsoccreatives_script'),
    path('run_T4wandtonicrsoctab3days_script/', views.run_T4wandtonicrsoctab3days_script, name='run_T4wandtonicrsoctab3days_script'),
    path('run_T5wandtonicrsoctabyes_script/', views.run_T5wandtonicrsoctabyes_script, name='run_T5wandtonicrsoctabyes_script'),
    path('run_T6wanduumrsoctonicoffers_script/', views.run_T6wanduumrsoctonicoffers_script, name='run_T6wanduumrsoctonicoffers_script'),
    path('run_newtabyes2wand_script/', views.run_newtabyes2wand_script, name='run_newtabyes2wand_script'),
    path('run_newtabyeswandnewfull_script/', views.run_newtabyeswandnewfull_script, name='run_newtabyeswandnewfull_script'),
    path('run_newtabyeswandnewfull_3click_script/', views.run_newtabyeswandnewfull_3click_script, name='run_newtabyeswandnewfull_3click_script'),
    path('run_tonic_wanduum_script/', views.run_tonic_wanduum_script, name='run_tonic_wanduum_script'),
    path('run_tonic_wanduum_3click_script/', views.run_tonic_wanduum_3click_script, name='run_tonic_wanduum_3click_script'),
    path('run_tonicEPCtrackingWand_script/', views.run_tonicEPCtrackingWand_script, name='run_tonicEPCtrackingWand_script'),
    path('run_tonicwandforopt_script/', views.run_tonicwandforopt_script, name='run_tonicwandforopt_script'),
    path('run_tonicwanduumnew3finals_new_script/', views.run_tonicwanduumnew3finals_new_script, name='run_tonicwanduumnew3finals_new_script'),
    path('run_Wanduum_Rsoc_copy_script/', views.run_Wanduum_Rsoc_copy_script, name='run_Wanduum_Rsoc_copy_script'),

    # Taboola page - Tonic Rsoc

    path('run_newtabyesrsoctonic_script/', views.run_newtabyesrsoctonic_script, name='run_newtabyesrsoctonic_script'),
    path('run_rsoctonicapple_script/', views.run_rsoctonicapple_script, name='run_rsoctonicapple_script'),


    # Taboola page - Inuvo

    path('run_inuvonewtabyes_script/', views.run_inuvonewtabyes_script, name='run_inuvonewtabyes_script'),
    path('run_inuvoyes_script/', views.run_inuvoyes_script, name='run_inuvoyes_script'),


    # Taboola page - Explore

    path('run_newtabyesexp_script/', views.run_newtabyesexp_script, name='run_newtabyesexp_script'),
    path('run_texplore1_script/', views.run_texplore1_script, name='run_texplore1_script'),




    # Compliance


    path('run_gettingtaboolarsocids_script/', views.run_gettingtaboolarsocids_script, name='run_gettingtaboolarsocids_script'),
    path('run_taboola_appealcompliancetonic_script/', views.run_taboola_appealcompliancetonic_script, name='run_taboola_appealcompliancetonic_script'),
    path('run_taboola_getcomplianceidsfromtonic_script/', views.run_taboola_getcomplianceidsfromtonic_script, name='run_taboola_getcomplianceidsfromtonic_script'),
    path('run_taboolacomplianceupdater2025_script/', views.run_taboolacomplianceupdater2025_script, name='run_taboolacomplianceupdater2025_script'),




    # Inuvo Compliance


    path('run_gettingtaboolainuvoids_2025_script/', views.run_gettingtaboolainuvoids_2025_script, name='run_gettingtaboolainuvoids_2025_script'),
    path('run_taboolacomplianceupdater_inuvo_2025_script/', views.run_taboolacomplianceupdater_inuvo_2025_script, name='run_taboolacomplianceupdater_inuvo_2025_script'),
    path('run_taboola_getcomplianceidsfrominuvo_script/', views.run_taboola_getcomplianceidsfrominuvo_script, name='run_taboola_getcomplianceidsfrominuvo_script'),




    # Tonic Compliance


    path('run_gettingtaboolarsocids2026_script/', views.run_gettingtaboolarsocids2026_script, name='run_gettingtaboolarsocids2026_script'),
    path('run_taboola_getcomplianceids_tonic2026_script/', views.run_taboola_getcomplianceids_tonic2026_script, name='run_taboola_getcomplianceids_tonic2026_script'),
    path('run_taboolacomplianceupdate2026_script/', views.run_taboolacomplianceupdate2026_script, name='run_taboolacomplianceupdate2026_script'),



################### Mediago page



    path('run_System_Report_MG_1_script/', views.run_System_Report_MG_1_script, name='run_System_Report_MG_1_script'),
    path('run_mediagocreatecmp_1_script/', views.run_mediagocreatecmp_1_script, name='run_mediagocreatecmp_1_script'),
    path('run_mediagogetallcampaigns_1_script/', views.run_mediagogetallcampaigns_1_script, name='run_mediagogetallcampaigns_1_script'),
    path('run_mediagoyes_1_script/', views.run_mediagoyes_1_script, name='run_mediagoyes_1_script'),
    path('run_mediagocreatives_script/', views.run_mediagocreatives_script, name='run_mediagocreatives_script'),
    path('run_mediagoopt_script/', views.run_mediagoopt_script, name='run_mediagoopt_script'),

    path('run_mediagoyesinuvo_script/', views.run_mediagoyesinuvo_script, name='run_mediagoyesinuvo_script'),
    path('run_mediagogetallcampaignsinuvo_script/', views.run_mediagogetallcampaignsinuvo_script, name='run_mediagogetallcampaignsinuvo_script'),
    path('run_inuvoyes_mediago_script/', views.run_inuvoyes_mediago_script, name='run_inuvoyes_mediago_script'),
    path('run_mediagooptinuvo_script/', views.run_mediagooptinuvo_script, name='run_mediagooptinuvo_script'),
    path('run_mediagoinuvocreatives_script/', views.run_mediagoinuvocreatives_script, name='run_mediagoinuvocreatives_script'),
    path('run_mediagocreatecmpnewinuvo_script/', views.run_mediagocreatecmpnewinuvo_script, name='run_mediagocreatecmpnewinuvo_script'),



    # Compliance


    path('run_gettingtaboolarsocidsformediago_script/', views.run_gettingtaboolarsocidsformediago_script, name='run_gettingtaboolarsocidsformediago_script'),
    path('run_getcreativesfromtaboolatomediago_script/', views.run_getcreativesfromtaboolatomediago_script, name='run_getcreativesfromtaboolatomediago_script'),
    path('run_mediago_getcomplianceidsfromtonic_script/', views.run_mediago_getcomplianceidsfromtonic_script, name='run_mediago_getcomplianceidsfromtonic_script'),

    path('run_mediago_getcomplianceforbulkfile_script/', views.run_mediago_getcomplianceforbulkfile_script, name='run_mediago_getcomplianceforbulkfile_script'),
    path('run_uploadtabformediago_script/', views.run_uploadtabformediago_script, name='run_uploadtabformediago_script'),
    path('run_uploadtabitemsformediago_script/', views.run_uploadtabitemsformediago_script, name='run_uploadtabitemsformediago_script'),


    path('run_MediaGo_Daily_Spend_PAW_script/', views.run_MediaGo_Daily_Spend_PAW_script, name='run_MediaGo_Daily_Spend_PAW_script'),
    path('run_MediaGo_Creative_PAW_script/', views.run_MediaGo_Creative_PAW_script, name='run_MediaGo_Creative_PAW_script'),
    path('run_MediaGo_All_Campaigns_PAW_script/', views.run_MediaGo_All_Campaigns_PAW_script, name='run_MediaGo_All_Campaigns_PAW_script'),
    path('run_MediaGo_Opt_PAW_script/', views.run_MediaGo_Opt_PAW_script, name='run_MediaGo_Opt_PAW_script'),


################### Poppin page


    path('run_poppintonic_script/', views.run_poppintonic_script, name='run_poppintonic_script'),
    path('run_poppinyes_script/', views.run_poppinyes_script, name='run_poppinyes_script'),
    path('run_tonic_poppinoffers_script/', views.run_tonic_poppinoffers_script, name='run_tonic_poppinoffers_script'),
    path('run_poppintonic_L7_script/', views.run_poppintonic_L7_script, name='run_poppintonic_L7_script'),
    path('run_poppincreatecmp2_script/', views.run_poppincreatecmp2_script, name='run_poppincreatecmp2_script'),
    path('run_rsoctoniccreateofferspoppin_script/', views.run_rsoctoniccreateofferspoppin_script, name='run_rsoctoniccreateofferspoppin_script'),

    path('run_Poppin_Opt_PAW_script/', views.run_Poppin_Opt_PAW_script, name='run_Poppin_Opt_PAW_script'),
    path('run_Poppin_Upload_PAW_script/', views.run_Poppin_Upload_PAW_script, name='run_Poppin_Upload_PAW_script'),
    path('run_Poppin_Daily_Spend_PAW_script/', views.run_Poppin_Daily_Spend_PAW_script, name='run_Poppin_Daily_Spend_PAW_script'),
    path('run_Poppin_Creative_PAW_script/', views.run_Poppin_Creative_PAW_script, name='run_Poppin_Creative_PAW_script'),


    # Poppin X page

    path('Poppin_X_page/', views.Poppin_X_page, name='Poppin_X_page'),
    path('run_tonic_poppinXoffers_script/', views.run_tonic_poppinXoffers_script, name='run_tonic_poppinXoffers_script'),
    path('run_set_poppinXoffers_callback_script/', views.run_set_poppinXoffers_callback_script, name='run_set_poppinXoffers_callback_script'),
    path('run_rsoctoniccreateofferspoppinX_script/', views.run_rsoctoniccreateofferspoppinX_script, name='run_rsoctoniccreateofferspoppinX_script'),
    path('run_poppinX_tonic_daily_script/', views.run_poppinX_tonic_daily_script, name='run_poppinX_tonic_daily_script'),


################### Outbrain page


    path('run_Outbrain_14_X_script/', views.run_Outbrain_14_X_script, name='run_Outbrain_14_X_script'),
    path('run_obyesinuvo_script/', views.run_obyesinuvo_script, name='run_obyesinuvo_script'),
    path('run_inuvoyesob_script/', views.run_inuvoyesob_script, name='run_inuvoyesob_script'),
    path('run_obcreativesl14_script/', views.run_obcreativesl14_script, name='run_obcreativesl14_script'),
    path('run_outbrainNeedToArchive_script/', views.run_outbrainNeedToArchive_script, name='run_outbrainNeedToArchive_script'),
    path('run_obnospendl14_script/', views.run_obnospendl14_script, name='run_obnospendl14_script'),
    path('run_obyes_script/', views.run_obyes_script, name='run_obyes_script'),



    # Compliance


    path('run_outbrain_appealcompliancetonic_script/', views.run_outbrain_appealcompliancetonic_script, name='run_outbrain_appealcompliancetonic_script'),
    path('run_outbrain_appealcompliancetonic_NewStuff_script/', views.run_outbrain_appealcompliancetonic_NewStuff_script, name='run_outbrain_appealcompliancetonic_NewStuff_script'),
    path('run_outbrain_getcomplianceidsfromtonic_script/', views.run_outbrain_getcomplianceidsfromtonic_script, name='run_outbrain_getcomplianceidsfromtonic_script'),
    path('run_outbraincomplianceupdater2025_script/', views.run_outbraincomplianceupdater2025_script, name='run_outbraincomplianceupdater2025_script'),



    # Opt


    path('run_outbrainopt2026_script/', views.run_outbrainopt2026_script, name='run_outbrainopt2026_script'),



################### Facebook page


    path('run_allfbcreatives_script/', views.run_allfbcreatives_script, name='run_allfbcreatives_script'),
    path('run_inuvoyes_newmobile2025api_script/', views.run_inuvoyes_newmobile2025api_script, name='run_inuvoyes_newmobile2025api_script'),
    path('run_inuvoopt_script/', views.run_inuvoopt_script, name='run_inuvoopt_script'),
    path('run_tonic_fboffers_script/', views.run_tonic_fboffers_script, name='run_tonic_fboffers_script'),
    path('run_dailyfb_script/', views.run_dailyfb_script, name='run_dailyfb_script'),
    path('run_fbopt2026_script/', views.run_fbopt2026_script, name='run_fbopt2026_script'),


    # Compliance


    path('run_facebook_appealcompliancetonic_script/', views.run_facebook_appealcompliancetonic_script, name='run_facebook_appealcompliancetonic_script'),
    path('run_facebook_getcomplianceidsfromtonic_script/', views.run_facebook_getcomplianceidsfromtonic_script, name='run_facebook_getcomplianceidsfromtonic_script'),
    path('run_facebookcomplianceupdater2025_script/', views.run_facebookcomplianceupdater2025_script, name='run_facebookcomplianceupdater2025_script'),
    path('run_facebookcomplianceupdater2025_v2_script/', views.run_facebookcomplianceupdater2025_v2_script, name='run_facebookcomplianceupdater2025_v2_script'),
    path('run_getfbtonicids_script/', views.run_getfbtonicids_script, name='run_getfbtonicids_script'),
    path('run_facebookcomplianceupdater2025_v3_script/', views.run_facebookcomplianceupdater2025_v3_script, name='run_facebookcomplianceupdater2025_v3_script'),


    # Reports


    path('run_FB_GGSH_script/', views.run_FB_GGSH_script, name='run_FB_GGSH_script'),

################### Twitter page


    path('run_inuvoyes_new2025api_script/', views.run_inuvoyes_new2025api_script, name='run_inuvoyes_new2025api_script'),
    path('run_twitter_createcmp2025_script/', views.run_twitter_createcmp2025_script, name='run_twitter_createcmp2025_script'),
    path('run_twitteropt_script/', views.run_twitteropt_script, name='run_twitteropt_script'),
    path('run_twitterreports_script/', views.run_twitterreports_script, name='run_twitterreports_script'),
    path('run_twitteryes_script/', views.run_twitteryes_script, name='run_twitteryes_script'),



################### Maximizer page


    path('run_maximizer_createoffer_script/', views.run_maximizer_createoffer_script, name='run_maximizer_createoffer_script'),
    path('run_maximizer_offersandverticals_script/', views.run_maximizer_offersandverticals_script, name='run_maximizer_offersandverticals_script'),
    path('run_maximizerrevsites30days_script/', views.run_maximizerrevsites30days_script, name='run_maximizerrevsites30days_script'),
    path('run_maximizerrevyes_script/', views.run_maximizerrevyes_script, name='run_maximizerrevyes_script'),
    path('run_newtabyesmaximizer_script/', views.run_newtabyesmaximizer_script, name='run_newtabyesmaximizer_script'),
    path('run_tabautoopt_maximizer_script/', views.run_tabautoopt_maximizer_script, name='run_tabautoopt_maximizer_script'),



################### Google page


    path('run_googleadsyesspend_script/', views.run_googleadsyesspend_script, name='run_googleadsyesspend_script'),
    path('run_googleadscomb2_script/', views.run_googleadscomb2_script, name='run_googleadscomb2_script'),
    path('run_googleurls_script/', views.run_googleurls_script, name='run_googleurls_script'),
    path('run_rsoctonicoffersggl_script/', views.run_rsoctonicoffersggl_script, name='run_rsoctonicoffersggl_script'),
    path('run_gglpctsmax_script/', views.run_gglpctsmax_script, name='run_gglpctsmax_script'),
    path('run_gglpctsdemandgen_script/', views.run_gglpctsdemandgen_script, name='run_gglpctsdemandgen_script'),
    path('run_googleopt2026_script/', views.run_googleopt2026_script, name='run_googleopt2026_script'),
    path('run_googleopt2026_shz_script/', views.run_googleopt2026_shz_script, name='run_googleopt2026_shz_script'),


    path('run_allgoogleyes_v2_script/', views.run_allgoogleyes_v2_script, name='run_allgoogleyes_v2_script'),
    path('run_googlenospendl7days_script/', views.run_googlenospendl7days_script, name='run_googlenospendl7days_script'),
    path('run_allgoogleyes_v2_Shinez_script/', views.run_allgoogleyes_v2_Shinez_script, name='run_allgoogleyes_v2_Shinez_script'),
    path('run_googlenospendl7days_Shinez_script/', views.run_googlenospendl7days_Shinez_script, name='run_googlenospendl7days_Shinez_script'),


    # Compliance


    path('run_gettingtaboolarsocidsforgoogle_script/', views.run_gettingtaboolarsocidsforgoogle_script, name='run_gettingtaboolarsocidsforgoogle_script'),
    path('run_google_getcomplianceidsfromtonic_script/', views.run_google_getcomplianceidsfromtonic_script, name='run_google_getcomplianceidsfromtonic_script'),
    path('run_getcreativesfromtaboolatogoogle_script/', views.run_getcreativesfromtaboolatogoogle_script, name='run_getcreativesfromtaboolatogoogle_script'),
    path('run_blockplacementsonggl_script/', views.run_blockplacementsonggl_script, name='run_blockplacementsonggl_script'),
    path('run_googlerejectl7days_script/', views.run_googlerejectl7days_script, name='run_googlerejectl7days_script'),
    path('run_googleappeal7days_script/', views.run_googleappeal7days_script, name='run_googleappeal7days_script'),


    # Send To Taboola


    path('run_uploadtabforgenfile_script/', views.run_uploadtabforgenfile_script, name='run_uploadtabforgenfile_script'),
    path('run_uploadtabitemsforgenfile_script/', views.run_uploadtabitemsforgenfile_script, name='run_uploadtabitemsforgenfile_script'),
    path('run_genfile_getcomplianceresults_script/', views.run_genfile_getcomplianceresults_script, name='run_genfile_getcomplianceresults_script'),


################### Newsbreak page



    path('run_rsoctoniccreateofferesnewsbreak_script/', views.run_rsoctoniccreateofferesnewsbreak_script, name='run_rsoctoniccreateofferesnewsbreak_script'),
    path('run_tonic_newsbreakoffers_script/', views.run_tonic_newsbreakoffers_script, name='run_tonic_newsbreakoffers_script'),
    path('run_set_callback_script/', views.run_set_callback_script, name='run_set_callback_script'),
    path('run_newsbreakopt1_script/', views.run_newsbreakopt1_script, name='run_newsbreakopt1_script'),
    path('run_newsbreakuploader_script/', views.run_newsbreakuploader_script, name='run_newsbreakuploader_script'),
    path('run_newsbreakadsetdaily_script/', views.run_newsbreakadsetdaily_script, name='run_newsbreakadsetdaily_script'),
    path('run_newsbreakadsetsdata_script/', views.run_newsbreakadsetsdata_script, name='run_newsbreakadsetsdata_script'),
    path('run_newsbreakdaily2_script/', views.run_newsbreakdaily2_script, name='run_newsbreakdaily2_script'),




################### Bulk - Creative




    path('run_DescriptionGPT_script/', views.run_DescriptionGPT_script, name='run_DescriptionGPT_script'),
    path('run_Google__ImagesCutHeadlines3_script/', views.run_Google__ImagesCutHeadlines3_script, name='run_Google__ImagesCutHeadlines3_script'),
    path('run_GoogleHeadlines3_script/', views.run_GoogleHeadlines3_script, name='run_GoogleHeadlines3_script'),
    path('run_MediaGOAutoGPT_script/', views.run_MediaGOAutoGPT_script, name='run_MediaGOAutoGPT_script'),
    path('run_MediaGoCreateAndCutImg_script/', views.run_MediaGoCreateAndCutImg_script, name='run_MediaGoCreateAndCutImg_script'),

    path('run_KWCityCheck_script/', views.run_KWCityCheck_script, name='run_KWCityCheck_script'),
    path('run_videotozapcap_script/', views.run_videotozapcap_script, name='run_videotozapcap_script'),
    path('run_Symphony_create_script/', views.run_Symphony_create_script, name='run_Symphony_create_script'),
    path('run_FKGCreateKW_script/', views.run_FKGCreateKW_script, name='run_FKGCreateKW_script'),
    path('run_VertCertDB_script/', views.run_VertCertDB_script, name='run_VertCertDB_script'),
    path('run_PolicyCheck_script/', views.run_PolicyCheck_script, name='run_PolicyCheck_script'),
    path('run_MediaGo_ShortHeadlines_script/', views.run_MediaGo_ShortHeadlines_script, name='run_MediaGo_ShortHeadlines_script'),
    path('run_MatanKWdecoder_script/', views.run_MatanKWdecoder_script, name='run_MatanKWdecoder_script'),

    path('run_creative_bulk_newpolicycheckforall_script/', views.run_creative_bulk_newpolicycheckforall_script, name='run_creative_bulk_newpolicycheckforall_script'),

    path('run_Jenia_creatives_builder_script/', views.run_Jenia_creatives_builder_script, name='run_Jenia_creatives_builder_script'),
    path('run_Jenia2_creatives_builder_script/', views.run_Jenia2_creatives_builder_script, name='run_Jenia2_creatives_builder_script'),
    path('run_Jenia3_creatives_builder_script/', views.run_Jenia3_creatives_builder_script, name='run_Jenia3_creatives_builder_script'),


    ######




    path('run_AutoCreativesWArsocHeadlines_script/', views.run_AutoCreativesWArsocHeadlines_script, name='run_AutoCreativesWArsocHeadlines_script'),
    path('run_WARSOC_Auto_Creative_Create_IMG_script/', views.run_WARSOC_Auto_Creative_Create_IMG_script, name='run_WARSOC_Auto_Creative_Create_IMG_script'),
    path('run_WARSOC_Auto_Creative_Split_IMG_script/', views.run_WARSOC_Auto_Creative_Split_IMG_script, name='run_WARSOC_Auto_Creative_Split_IMG_script'),

    path('run_AutoCreativesWARSOC1_script/', views.run_AutoCreativesWARSOC1_script, name='run_AutoCreativesWARSOC1_script'),
    path('run_AutoCreativesWARSOC2_script/', views.run_AutoCreativesWARSOC2_script, name='run_AutoCreativesWARSOC2_script'),
    path('run_AutoCreativesWARSOC3_script/', views.run_AutoCreativesWARSOC3_script, name='run_AutoCreativesWARSOC3_script'),

    ######



    path('run_Danilo_videotozapcap_script/', views.run_Danilo_videotozapcap_script, name='run_Danilo_videotozapcap_script'),
    path('run_Danilo_Symphony_create_script/', views.run_Danilo_Symphony_create_script, name='run_Danilo_Symphony_create_script'),


    ######



    path('run_Jenia_newpolicycheckforall_script/', views.run_Jenia_newpolicycheckforall_script, name='run_Jenia_newpolicycheckforall_script'),
    path('run_Jenia_googlepolicychecker_script/', views.run_Jenia_googlepolicychecker_script, name='run_Jenia_googlepolicychecker_script'),
    path('run_Jenia_gcpgetdataforjenia_script/', views.run_Jenia_gcpgetdataforjenia_script, name='run_Jenia_gcpgetdataforjenia_script'),


    ######



    path('run_blastfromthepast_gettaboolacreatives_script/', views.run_blastfromthepast_gettaboolacreatives_script, name='run_blastfromthepast_gettaboolacreatives_script'),
    path('run_blastfromthepast_getoutbraincreatives_script/', views.run_blastfromthepast_getoutbraincreatives_script, name='run_blastfromthepast_getoutbraincreatives_script'),
    path('run_blastfromthepast_getgooglecreatives_script/', views.run_blastfromthepast_getgooglecreatives_script, name='run_blastfromthepast_getgooglecreatives_script'),
    path('run_blastfromthepast_getfacebookcreatives_script/', views.run_blastfromthepast_getfacebookcreatives_script, name='run_blastfromthepast_getfacebookcreatives_script'),
    path('run_getolddatafromfiles_script/', views.run_getolddatafromfiles_script, name='run_getolddatafromfiles_script'),


    ######


    path('run_Jenia_newautogptforpanglework_script/', views.run_Jenia_newautogptforpanglework_script, name='run_Jenia_newautogptforpanglework_script'),
    path('run_Jenia_keywordsitallpangle2025_script/', views.run_Jenia_keywordsitallpangle2025_script, name='run_Jenia_keywordsitallpangle2025_script'),



################### Tiktok




    path('run_TKTRSOCARTICLEUPDATE_script/', views.run_TKTRSOCARTICLEUPDATE_script, name='run_TKTRSOCARTICLEUPDATE_script'),
    path('run_imagegenreationautotiktok_script/', views.run_imagegenreationautotiktok_script, name='run_imagegenreationautotiktok_script'),
    path('run_tonic_tiktokoffers_script/', views.run_tonic_tiktokoffers_script, name='run_tonic_tiktokoffers_script'),


    path('run_video_newpolicycheckforall_script/', views.run_video_newpolicycheckforall_script, name='run_video_newpolicycheckforall_script'),

    ####


    path('run_Danilo_tonic_tiktokoffers_script/', views.run_Danilo_tonic_tiktokoffers_script, name='run_Danilo_tonic_tiktokoffers_script'),

    ####


    path('run_imagecreativesforvideo_script/', views.run_imagecreativesforvideo_script, name='run_imagecreativesforvideo_script'),



    # Compliance


    path('run_tiktok_appealcompliancetonic_script/', views.run_tiktok_appealcompliancetonic_script, name='run_tiktok_appealcompliancetonic_script'),
    path('run_tiktok_getcomplianceidsfromtonic_script/', views.run_tiktok_getcomplianceidsfromtonic_script, name='run_tiktok_getcomplianceidsfromtonic_script'),
    path('run_tkactivateads_script/', views.run_tkactivateads_script, name='run_tkactivateads_script'),
    path('run_tkpauseads_script/', views.run_tkpauseads_script, name='run_tkpauseads_script'),
    path('run_gettiktokids_script/', views.run_gettiktokids_script, name='run_gettiktokids_script'),


    # Opt data update


    path('run_pangeupdate_only4days_script/', views.run_pangeupdate_only4days_script, name='run_pangeupdate_only4days_script'),
    path('run_updatepangleoptdata_script/', views.run_updatepangleoptdata_script, name='run_updatepangleoptdata_script'),


    # Video URL converter


    path('run_gcptoawsvideoconvert_jenia_script/', views.run_gcptoawsvideoconvert_jenia_script, name='run_gcptoawsvideoconvert_jenia_script'),
    path('run_gcptoawsvideoconvert_maya_script/', views.run_gcptoawsvideoconvert_maya_script, name='run_gcptoawsvideoconvert_maya_script'),
    path('run_gcptoawsvideoconvert_elran_script/', views.run_gcptoawsvideoconvert_elran_script, name='run_gcptoawsvideoconvert_elran_script'),
    path('run_gcptoawsvideoconvert_Omer_script/', views.run_gcptoawsvideoconvert_Omer_script, name='run_gcptoawsvideoconvert_Omer_script'),
    path('run_gcptoawsvideoconvert_matan_script/', views.run_gcptoawsvideoconvert_matan_script, name='run_gcptoawsvideoconvert_matan_script'),





################### Amir




    path('run_MJ_Stock_Generator_V1_script/', views.run_MJ_Stock_Generator_V1_script, name='run_MJ_Stock_Generator_V1_script'),





################### Sharon




    path('run_allweeklyupdate_script/', views.run_allweeklyupdate_script, name='run_allweeklyupdate_script'),





################### MGID




    path('run_mgidrsoctoniccreate_link_callback_script/', views.run_mgidrsoctoniccreate_link_callback_script, name='run_mgidrsoctoniccreate_link_callback_script'),
    path('run_mgid_active_tonic_campaigns_script/', views.run_mgid_active_tonic_campaigns_script, name='run_mgid_active_tonic_campaigns_script'),



################### Duplicator




    # Taboola Duplicator



    path('run_getalltaboolaidsfordup_script/', views.run_getalltaboolaidsfordup_script, name='run_getalltaboolaidsfordup_script'),
    path('run_getallcreativesfortabooladup_script/', views.run_getallcreativesfortabooladup_script, name='run_getallcreativesfortabooladup_script'),
    path('run_getallcampaignsdatafordup_script/', views.run_getallcampaignsdatafordup_script, name='run_getallcampaignsdatafordup_script'),



    # Outbrain Duplicator



    path('run_getallcampaigndetailsforoutbraindup_script/', views.run_getallcampaigndetailsforoutbraindup_script, name='run_getallcampaigndetailsforoutbraindup_script'),
    path('run_getallcreativesforoutbraindup_script/', views.run_getallcreativesforoutbraindup_script, name='run_getallcreativesforoutbraindup_script'),



    # Facebook Duplicator



    path('run_getallfbcreativesfordup_script/', views.run_getallfbcreativesfordup_script, name='run_getallfbcreativesfordup_script'),
    path('run_getallfbdata_script/', views.run_getallfbdata_script, name='run_getallfbdata_script'),
    path('run_tonicforfb_script/', views.run_tonicforfb_script, name='run_tonicforfb_script'),




    # Mediago Duplicator



    path('run_copymediagodata_script/', views.run_copymediagodata_script, name='run_copymediagodata_script'),



    # Poppin Duplicator



    path('run_copypoppindata_script/', views.run_copypoppindata_script, name='run_copypoppindata_script'),



    # Google Duplicator



    path('run_l4daysgoogleduplicatordata_script/', views.run_l4daysgoogleduplicatordata_script, name='run_l4daysgoogleduplicatordata_script'),



    # Wthmm completer



    path('run_wthmmduplicatorupdate_script/', views.run_wthmmduplicatorupdate_script, name='run_wthmmduplicatorupdate_script'),
    path('run_wthmmcompleter_script/', views.run_wthmmcompleter_script, name='run_wthmmcompleter_script'),



    path('run_wthmmduplicatorupdate_Google_script/', views.run_wthmmduplicatorupdate_Google_script, name='run_wthmmduplicatorupdate_Google_script'),
    path('run_wthmmduplicatorupdate_FB_script/', views.run_wthmmduplicatorupdate_FB_script, name='run_wthmmduplicatorupdate_FB_script'),
    path('run_wthmmduplicatorupdate_Taboola_script/', views.run_wthmmduplicatorupdate_Taboola_script, name='run_wthmmduplicatorupdate_Taboola_script'),
    path('run_wthmmduplicatorupdate_Outbrain_script/', views.run_wthmmduplicatorupdate_Outbrain_script, name='run_wthmmduplicatorupdate_Outbrain_script'),
    path('run_wthmmduplicatorupdate_Poppin_script/', views.run_wthmmduplicatorupdate_Poppin_script, name='run_wthmmduplicatorupdate_Poppin_script'),
    path('run_wthmmduplicatorupdate_MediaGo_script/', views.run_wthmmduplicatorupdate_MediaGo_script, name='run_wthmmduplicatorupdate_MediaGo_script'),
    path('run_wthmmduplicatorupdate_TikTok_script/', views.run_wthmmduplicatorupdate_TikTok_script, name='run_wthmmduplicatorupdate_TikTok_script'),






################### GPT Executor and Part 1/2 pages



    path('gpt_executor/', views.gpt_executor_page, name='gpt_executor_page'),
    path('gpt_part1/', views.gpt_part1_page, name='gpt_part1_page'),
    path('gpt_part2/', views.gpt_part2_page, name='gpt_part2_page'),

    # Script actions for Part 1
    path('run-gpt-part1/', views.run_gpt_part1_script, name='run_gpt_part1_script'),
    path('stop-gpt-part1/', views.stop_gpt_part1_script, name='stop_gpt_part1_script'),

    # Script actions for Part 2
    path('run-gpt-part2/', views.run_gpt_part2_script, name='run_gpt_part2_script'),
    path('stop-gpt-part2/', views.stop_gpt_part2_script, name='stop_gpt_part2_script'),

    path('process_form/', views.process_form_page, name='process_form_page'),
    path('stop_script/', views.stop_script, name='stop_script'),  # New URL for stopping the script



################### Karmel page


    path('run-facebook/', views.run_facebook_script, name='run_facebook_script'),
    path('run-google/', views.run_google_script, name='run_google_script'),
    path('run-tiktok/', views.run_tiktok_script, name='run_tiktok_script'),
    path('run-outbrain/', views.run_outbrain_script, name='run_outbrain_script'),




################### Passwords section #############



    # Password prompt views for protected pages
    path('amit_scripts_password/', views.amit_scripts_password, name='amit_scripts_password'),
    path('mediago_password/', views.mediago_password, name='mediago_password'),
    path('outbrain_password/', views.outbrain_password, name='outbrain_password'),
    path('zemanta_password/', views.zemanta_password, name='zemanta_password'),
    path('taboola_password/', views.taboola_password, name='taboola_password'),
    path('poppin_password/', views.poppin_password, name='poppin_password'),





################### Taboola page



    # Taboola page - Bulk

    path('taboola_Bulk/', views.taboola_Bulk_page, name='taboola_Bulk_page'),
    path('run_bulk_tonic_taboolaoffers_script/', views.run_bulk_tonic_taboolaoffers_script, name='run_bulk_tonic_taboolaoffers_script'),
    path('run_bulk_rsoctoniccreateofferestaboola_script/', views.run_bulk_rsoctoniccreateofferestaboola_script, name='run_bulk_rsoctoniccreateofferestaboola_script'),
    path('run_bulk_maxbidstaboola_UPCPCS1_script/', views.run_bulk_maxbidstaboola_UPCPCS1_script, name='run_bulk_maxbidstaboola_UPCPCS1_script'),
    path('run_bulk_maxbidstaboola_UPCPCRSOC_script/', views.run_bulk_maxbidstaboola_UPCPCRSOC_script, name='run_bulk_maxbidstaboola_UPCPCRSOC_script'),
    path('run_bulk_maxbidstaboola_UPCPC_script/', views.run_bulk_maxbidstaboola_UPCPC_script, name='run_bulk_maxbidstaboola_UPCPC_script'),
    path('run_bulk_maxbidstaboola_UPCPCINU_script/', views.run_bulk_maxbidstaboola_UPCPCINU_script, name='run_bulk_maxbidstaboola_UPCPCINU_script'),

    path('run_bulk_tabduplicatorfortest_s1_script/', views.run_bulk_tabduplicatorfortest_s1_script, name='run_bulk_tabduplicatorfortest_s1_script'),
    path('run_bulk_tabduplicatorfortest_Inuvo_script/', views.run_bulk_tabduplicatorfortest_Inuvo_script, name='run_bulk_tabduplicatorfortest_Inuvo_script'),
    path('run_bulk_tabduplicatorfortest_AFD_script/', views.run_bulk_tabduplicatorfortest_AFD_script, name='run_bulk_tabduplicatorfortest_AFD_script'),
    path('run_bulk_tabduplicatorfortest_RSOC_script/', views.run_bulk_tabduplicatorfortest_RSOC_script, name='run_bulk_tabduplicatorfortest_RSOC_script'),
    path('run_bulk_tabduplicatorfortest_TC_script/', views.run_bulk_tabduplicatorfortest_TC_script, name='run_bulk_tabduplicatorfortest_TC_script'),

    path('run_bulk_upload_taboola_creatives_S1_script/', views.run_bulk_upload_taboola_creatives_S1_script, name='run_bulk_upload_taboola_creatives_S1_script'),
    path('run_bulk_upload_taboola_creatives_TC_script/', views.run_bulk_upload_taboola_creatives_TC_script, name='run_bulk_upload_taboola_creatives_TC_script'),
    path('run_bulk_upload_taboola_creatives_RSOC_script/', views.run_bulk_upload_taboola_creatives_RSOC_script, name='run_bulk_upload_taboola_creatives_RSOC_script'),
    path('run_bulk_upload_taboola_creatives_Inuvo_script/', views.run_bulk_upload_taboola_creatives_Inuvo_script, name='run_bulk_upload_taboola_creatives_Inuvo_script'),


    path('run_taboola_bulk_newpolicycheckforall_script/', views.run_taboola_bulk_newpolicycheckforall_script, name='run_taboola_bulk_newpolicycheckforall_script'),

    path('run_taboola_bulk__tchannels_createnew_script/', views.run_taboola_bulk__tchannels_createnew_script, name='run_taboola_bulk__tchannels_createnew_script'),
    path('run_taboola_bulk__tchannelsdb_script/', views.run_taboola_bulk__tchannelsdb_script, name='run_taboola_bulk__tchannelsdb_script'),


    # Taboola page - Bulk2

    path('taboola_Bulk2/', views.taboola_Bulk2_page, name='taboola_Bulk2_page'),
    path('run_bulk2_tonic_taboolaoffers_script/', views.run_bulk2_tonic_taboolaoffers_script, name='run_bulk2_tonic_taboolaoffers_script'),
    path('run_bulk2_rsoctoniccreateofferestaboola_script/', views.run_bulk2_rsoctoniccreateofferestaboola_script, name='run_bulk2_rsoctoniccreateofferestaboola_script'),
    path('run_bulk2_maxbidstaboola_UPCPCS1_script/', views.run_bulk2_maxbidstaboola_UPCPCS1_script, name='run_bulk2_maxbidstaboola_UPCPCS1_script'),
    path('run_bulk2_maxbidstaboola_UPCPCRSOC_script/', views.run_bulk2_maxbidstaboola_UPCPCRSOC_script, name='run_bulk2_maxbidstaboola_UPCPCRSOC_script'),
    path('run_bulk2_maxbidstaboola_UPCPC_script/', views.run_bulk2_maxbidstaboola_UPCPC_script, name='run_bulk2_maxbidstaboola_UPCPC_script'),
    path('run_bulk2_maxbidstaboola_UPCPCINU_script/', views.run_bulk2_maxbidstaboola_UPCPCINU_script, name='run_bulk2_maxbidstaboola_UPCPCINU_script'),
    path('run_bulk2_FKG_R_script/', views.run_bulk2_FKG_R_script, name='run_bulk2_FKG_R_script'),
    path('run_bulk2_KWCity_R_script/', views.run_bulk2_KWCity_R_script, name='run_bulk2_KWCity_R_script'),

    path('run_bulk2_tabduplicatorfortest_s1_script/', views.run_bulk2_tabduplicatorfortest_s1_script, name='run_bulk2_tabduplicatorfortest_s1_script'),
    path('run_bulk2_tabduplicatorfortest_Inuvo_script/', views.run_bulk2_tabduplicatorfortest_Inuvo_script, name='run_bulk2_tabduplicatorfortest_Inuvo_script'),
    path('run_bulk2_tabduplicatorfortest_AFD_script/', views.run_bulk2_tabduplicatorfortest_AFD_script, name='run_bulk2_tabduplicatorfortest_AFD_script'),
    path('run_bulk2_tabduplicatorfortest_RSOC_script/', views.run_bulk2_tabduplicatorfortest_RSOC_script, name='run_bulk2_tabduplicatorfortest_RSOC_script'),


    # Taboola page - Bulk_3


    path('taboola_Bulk_3/', views.taboola_Bulk_3_page, name='taboola_Bulk_3_page'),
    path('run_Bulk_3_tonic_taboolaoffers_script/', views.run_Bulk_3_tonic_taboolaoffers_script, name='run_Bulk_3_tonic_taboolaoffers_script'),
    path('run_Bulk_3_rsoctoniccreateofferestaboola_script/', views.run_Bulk_3_rsoctoniccreateofferestaboola_script, name='run_Bulk_3_rsoctoniccreateofferestaboola_script'),
    path('run_Bulk_3_maxbidstaboola_UPCPCS1_script/', views.run_Bulk_3_maxbidstaboola_UPCPCS1_script, name='run_Bulk_3_maxbidstaboola_UPCPCS1_script'),
    path('run_Bulk_3_maxbidstaboola_UPCPCRSOC_script/', views.run_Bulk_3_maxbidstaboola_UPCPCRSOC_script, name='run_Bulk_3_maxbidstaboola_UPCPCRSOC_script'),
    path('run_Bulk_3_maxbidstaboola_UPCPC_script/', views.run_Bulk_3_maxbidstaboola_UPCPC_script, name='run_Bulk_3_maxbidstaboola_UPCPC_script'),
    path('run_Bulk_3_maxbidstaboola_UPCPCINU_script/', views.run_Bulk_3_maxbidstaboola_UPCPCINU_script, name='run_Bulk_3_maxbidstaboola_UPCPCINU_script'),

    path('run_Bulk_3_tabduplicatorfortest_s1_script/', views.run_Bulk_3_tabduplicatorfortest_s1_script, name='run_Bulk_3_tabduplicatorfortest_s1_script'),
    path('run_Bulk_3_tabduplicatorfortest_Inuvo_script/', views.run_Bulk_3_tabduplicatorfortest_Inuvo_script, name='run_Bulk_3_tabduplicatorfortest_Inuvo_script'),
    path('run_Bulk_3_tabduplicatorfortest_AFD_script/', views.run_Bulk_3_tabduplicatorfortest_AFD_script, name='run_Bulk_3_tabduplicatorfortest_AFD_script'),
    path('run_Bulk_3_tabduplicatorfortest_RSOC_script/', views.run_Bulk_3_tabduplicatorfortest_RSOC_script, name='run_Bulk_3_tabduplicatorfortest_RSOC_script'),
    path('run_Bulk_3_tabduplicatorfortest_TC_script/', views.run_Bulk_3_tabduplicatorfortest_TC_script, name='run_Bulk_3_tabduplicatorfortest_TC_script'),


    path('run_Bulk_3_upload_taboola_creatives_S1_script/', views.run_Bulk_3_upload_taboola_creatives_S1_script, name='run_Bulk_3_upload_taboola_creatives_S1_script'),
    path('run_Bulk_3_upload_taboola_creatives_TC_script/', views.run_Bulk_3_upload_taboola_creatives_TC_script, name='run_Bulk_3_upload_taboola_creatives_TC_script'),
    path('run_Bulk_3_upload_taboola_creatives_RSOC_script/', views.run_Bulk_3_upload_taboola_creatives_RSOC_script, name='run_Bulk_3_upload_taboola_creatives_RSOC_script'),
    path('run_Bulk_3_upload_taboola_creatives_Inuvo_script/', views.run_Bulk_3_upload_taboola_creatives_Inuvo_script, name='run_Bulk_3_upload_taboola_creatives_Inuvo_script'),


    path('run_taboola_Bulk_3_newpolicycheckforall_script/', views.run_taboola_Bulk_3_newpolicycheckforall_script, name='run_taboola_Bulk_3_newpolicycheckforall_script'),

    path('run_taboola_Bulk_3__tchannels_createnew_script/', views.run_taboola_Bulk_3__tchannels_createnew_script, name='run_taboola_Bulk_3__tchannels_createnew_script'),
    path('run_taboola_Bulk_3__tchannelsdb_script/', views.run_taboola_Bulk_3__tchannelsdb_script, name='run_taboola_Bulk_3__tchannelsdb_script'),




    # Taboola page - Matan

    path('taboola_Matan/', views.taboola_Matan_page, name='taboola_Matan_page'),
    path('run_Matan_tonic_taboolaoffers_script/', views.run_Matan_tonic_taboolaoffers_script, name='run_Matan_tonic_taboolaoffers_script'),
    path('run_Matan_rsoctoniccreateofferestaboola_script/', views.run_Matan_rsoctoniccreateofferestaboola_script, name='run_Matan_rsoctoniccreateofferestaboola_script'),
    path('run_Matan_maxbidstaboola_UPCPCS1_script/', views.run_Matan_maxbidstaboola_UPCPCS1_script, name='run_Matan_maxbidstaboola_UPCPCS1_script'),
    path('run_Matan_maxbidstaboola_UPCPCRSOC_script/', views.run_Matan_maxbidstaboola_UPCPCRSOC_script, name='run_Matan_maxbidstaboola_UPCPCRSOC_script'),
    path('run_Matan_maxbidstaboola_UPCPC_script/', views.run_Matan_maxbidstaboola_UPCPC_script, name='run_Matan_maxbidstaboola_UPCPC_script'),
    path('run_Matan_maxbidstaboola_UPCPCINU_script/', views.run_Matan_maxbidstaboola_UPCPCINU_script, name='run_Matan_maxbidstaboola_UPCPCINU_script'),

    path('run_Matan_tabduplicatorfortest_s1_script/', views.run_Matan_tabduplicatorfortest_s1_script, name='run_Matan_tabduplicatorfortest_s1_script'),
    path('run_Matan_tabduplicatorfortest_Inuvo_script/', views.run_Matan_tabduplicatorfortest_Inuvo_script, name='run_Matan_tabduplicatorfortest_Inuvo_script'),
    path('run_Matan_tabduplicatorfortest_AFD_script/', views.run_Matan_tabduplicatorfortest_AFD_script, name='run_Matan_tabduplicatorfortest_AFD_script'),
    path('run_Matan_tabduplicatorfortest_RSOC_script/', views.run_Matan_tabduplicatorfortest_RSOC_script, name='run_Matan_tabduplicatorfortest_RSOC_script'),
    path('run_Matan_tabduplicatorfortest_TC_script/', views.run_Matan_tabduplicatorfortest_TC_script, name='run_Matan_tabduplicatorfortest_TC_script'),

    path('run_taboola_Matan_newpolicycheckforall_script/', views.run_taboola_Matan_newpolicycheckforall_script, name='run_taboola_Matan_newpolicycheckforall_script'),
    path('run_Matan_gcpgetdataforjenia_script/', views.run_Matan_gcpgetdataforjenia_script, name='run_Matan_gcpgetdataforjenia_script'),


    path('run_taboola_Matan__tchannels_createnew_script/', views.run_taboola_Matan__tchannels_createnew_script, name='run_taboola_Matan__tchannels_createnew_script'),
    path('run_taboola_Matan__tchannelsdb_script/', views.run_taboola_Matan__tchannelsdb_script, name='run_taboola_Matan__tchannelsdb_script'),

    # Taboola page - Omer

    path('taboola_Omer/', views.taboola_Omer_page, name='taboola_Omer_page'),
    path('run_Omer_tonic_taboolaoffers_script/', views.run_Omer_tonic_taboolaoffers_script, name='run_Omer_tonic_taboolaoffers_script'),
    path('run_Omer_rsoctoniccreateofferestaboola_script/', views.run_Omer_rsoctoniccreateofferestaboola_script, name='run_Omer_rsoctoniccreateofferestaboola_script'),
    path('run_Omer_maxbidstaboola_UPCPCS1_script/', views.run_Omer_maxbidstaboola_UPCPCS1_script, name='run_Omer_maxbidstaboola_UPCPCS1_script'),
    path('run_Omer_maxbidstaboola_UPCPCRSOC_script/', views.run_Omer_maxbidstaboola_UPCPCRSOC_script, name='run_Omer_maxbidstaboola_UPCPCRSOC_script'),
    path('run_Omer_maxbidstaboola_UPCPC_script/', views.run_Omer_maxbidstaboola_UPCPC_script, name='run_Omer_maxbidstaboola_UPCPC_script'),
    path('run_Omer_maxbidstaboola_UPCPCINU_script/', views.run_Omer_maxbidstaboola_UPCPCINU_script, name='run_Omer_maxbidstaboola_UPCPCINU_script'),

    path('run_Omer_tabduplicatorfortest_s1_script/', views.run_Omer_tabduplicatorfortest_s1_script, name='run_Omer_tabduplicatorfortest_s1_script'),
    path('run_Omer_tabduplicatorfortest_Inuvo_script/', views.run_Omer_tabduplicatorfortest_Inuvo_script, name='run_Omer_tabduplicatorfortest_Inuvo_script'),
    path('run_Omer_tabduplicatorfortest_AFD_script/', views.run_Omer_tabduplicatorfortest_AFD_script, name='run_Omer_tabduplicatorfortest_AFD_script'),
    path('run_Omer_tabduplicatorfortest_RSOC_script/', views.run_Omer_tabduplicatorfortest_RSOC_script, name='run_Omer_tabduplicatorfortest_RSOC_script'),
    path('run_Omer_tabduplicatorfortest_TC_script/', views.run_Omer_tabduplicatorfortest_TC_script, name='run_Omer_tabduplicatorfortest_TC_script'),

    path('run_taboola_Omer_newpolicycheckforall_script/', views.run_taboola_Omer_newpolicycheckforall_script, name='run_taboola_Omer_newpolicycheckforall_script'),
    path('run_Omer_gcpgetdataforjenia_script/', views.run_Omer_gcpgetdataforjenia_script, name='run_Omer_gcpgetdataforjenia_script'),


    path('run_taboola_Omer__tchannels_createnew_script/', views.run_taboola_Omer__tchannels_createnew_script, name='run_taboola_Omer__tchannels_createnew_script'),
    path('run_taboola_Omer__tchannelsdb_script/', views.run_taboola_Omer__tchannelsdb_script, name='run_taboola_Omer__tchannelsdb_script'),

    # Taboola page - Elad

    path('taboola_Elad/', views.taboola_Elad_page, name='taboola_Elad_page'),
    path('run_Elad_tonic_taboolaoffers_script/', views.run_Elad_tonic_taboolaoffers_script, name='run_Elad_tonic_taboolaoffers_script'),
    path('run_Elad_rsoctoniccreateofferestaboola_script/', views.run_Elad_rsoctoniccreateofferestaboola_script, name='run_Elad_rsoctoniccreateofferestaboola_script'),
    path('run_Elad_maxbidstaboola_UPCPCS1_script/', views.run_Elad_maxbidstaboola_UPCPCS1_script, name='run_Elad_maxbidstaboola_UPCPCS1_script'),
    path('run_Elad_maxbidstaboola_UPCPCRSOC_script/', views.run_Elad_maxbidstaboola_UPCPCRSOC_script, name='run_Elad_maxbidstaboola_UPCPCRSOC_script'),
    path('run_Elad_maxbidstaboola_UPCPC_script/', views.run_Elad_maxbidstaboola_UPCPC_script, name='run_Elad_maxbidstaboola_UPCPC_script'),
    path('run_Elad_maxbidstaboola_UPCPCINU_script/', views.run_Elad_maxbidstaboola_UPCPCINU_script, name='run_Elad_maxbidstaboola_UPCPCINU_script'),

    path('run_Elad_tabduplicatorfortest_s1_script/', views.run_Elad_tabduplicatorfortest_s1_script, name='run_Elad_tabduplicatorfortest_s1_script'),
    path('run_Elad_tabduplicatorfortest_Inuvo_script/', views.run_Elad_tabduplicatorfortest_Inuvo_script, name='run_Elad_tabduplicatorfortest_Inuvo_script'),
    path('run_Elad_tabduplicatorfortest_AFD_script/', views.run_Elad_tabduplicatorfortest_AFD_script, name='run_Elad_tabduplicatorfortest_AFD_script'),
    path('run_Elad_tabduplicatorfortest_RSOC_script/', views.run_Elad_tabduplicatorfortest_RSOC_script, name='run_Elad_tabduplicatorfortest_RSOC_script'),
    path('run_Elad_tabduplicatorfortest_TC_script/', views.run_Elad_tabduplicatorfortest_TC_script, name='run_Elad_tabduplicatorfortest_TC_script'),

    path('run_taboola_Elad_newpolicycheckforall_script/', views.run_taboola_Elad_newpolicycheckforall_script, name='run_taboola_Elad_newpolicycheckforall_script'),
    path('run_Elad_gcpgetdataforjenia_script/', views.run_Elad_gcpgetdataforjenia_script, name='run_Elad_gcpgetdataforjenia_script'),


    path('run_taboola_Elad__tchannels_createnew_script/', views.run_taboola_Elad__tchannels_createnew_script, name='run_taboola_Elad__tchannels_createnew_script'),
    path('run_taboola_Elad__tchannelsdb_script/', views.run_taboola_Elad__tchannelsdb_script, name='run_taboola_Elad__tchannelsdb_script'),



    path('run_Elad_upload_taboola_creatives_S1_script/', views.run_Elad_upload_taboola_creatives_S1_script, name='run_Elad_upload_taboola_creatives_S1_script'),
    path('run_Elad_upload_taboola_creatives_TC_script/', views.run_Elad_upload_taboola_creatives_TC_script, name='run_Elad_upload_taboola_creatives_TC_script'),
    path('run_Elad_upload_taboola_creatives_RSOC_script/', views.run_Elad_upload_taboola_creatives_RSOC_script, name='run_Elad_upload_taboola_creatives_RSOC_script'),
    path('run_Elad_upload_taboola_creatives_Inuvo_script/', views.run_Elad_upload_taboola_creatives_Inuvo_script, name='run_Elad_upload_taboola_creatives_Inuvo_script'),


    # Taboola page - Elran

    path('taboola_Elran/', views.taboola_Elran_page, name='taboola_Elran_page'),
    path('run_Elran_tonic_taboolaoffers_script/', views.run_Elran_tonic_taboolaoffers_script, name='run_Elran_tonic_taboolaoffers_script'),
    path('run_Elran_rsoctoniccreateofferestaboola_script/', views.run_Elran_rsoctoniccreateofferestaboola_script, name='run_Elran_rsoctoniccreateofferestaboola_script'),
    path('run_Elran_maxbidstaboola_UPCPCS1_script/', views.run_Elran_maxbidstaboola_UPCPCS1_script, name='run_Elran_maxbidstaboola_UPCPCS1_script'),
    path('run_Elran_maxbidstaboola_UPCPCRSOC_script/', views.run_Elran_maxbidstaboola_UPCPCRSOC_script, name='run_Elran_maxbidstaboola_UPCPCRSOC_script'),
    path('run_Elran_maxbidstaboola_UPCPC_script/', views.run_Elran_maxbidstaboola_UPCPC_script, name='run_Elran_maxbidstaboola_UPCPC_script'),
    path('run_Elran_maxbidstaboola_UPCPCINU_script/', views.run_Elran_maxbidstaboola_UPCPCINU_script, name='run_Elran_maxbidstaboola_UPCPCINU_script'),

    path('run_Elran_tabduplicatorfortest_s1_script/', views.run_Elran_tabduplicatorfortest_s1_script, name='run_Elran_tabduplicatorfortest_s1_script'),
    path('run_Elran_tabduplicatorfortest_Inuvo_script/', views.run_Elran_tabduplicatorfortest_Inuvo_script, name='run_Elran_tabduplicatorfortest_Inuvo_script'),
    path('run_Elran_tabduplicatorfortest_AFD_script/', views.run_Elran_tabduplicatorfortest_AFD_script, name='run_Elran_tabduplicatorfortest_AFD_script'),
    path('run_Elran_tabduplicatorfortest_RSOC_script/', views.run_Elran_tabduplicatorfortest_RSOC_script, name='run_Elran_tabduplicatorfortest_RSOC_script'),
    path('run_Elran_tabduplicatorfortest_TC_script/', views.run_Elran_tabduplicatorfortest_TC_script, name='run_Elran_tabduplicatorfortest_TC_script'),

    path('run_taboola_Elran_newpolicycheckforall_script/', views.run_taboola_Elran_newpolicycheckforall_script, name='run_taboola_Elran_newpolicycheckforall_script'),


    path('run_taboola_Elran__tchannels_createnew_script/', views.run_taboola_Elran__tchannels_createnew_script, name='run_taboola_Elran__tchannels_createnew_script'),
    path('run_taboola_Elran__tchannelsdb_script/', views.run_taboola_Elran__tchannelsdb_script, name='run_taboola_Elran__tchannelsdb_script'),



    path('run_Elran_upload_taboola_creatives_S1_script/', views.run_Elran_upload_taboola_creatives_S1_script, name='run_Elran_upload_taboola_creatives_S1_script'),
    path('run_Elran_upload_taboola_creatives_TC_script/', views.run_Elran_upload_taboola_creatives_TC_script, name='run_Elran_upload_taboola_creatives_TC_script'),
    path('run_Elran_upload_taboola_creatives_RSOC_script/', views.run_Elran_upload_taboola_creatives_RSOC_script, name='run_Elran_upload_taboola_creatives_RSOC_script'),
    path('run_Elran_upload_taboola_creatives_Inuvo_script/', views.run_Elran_upload_taboola_creatives_Inuvo_script, name='run_Elran_upload_taboola_creatives_Inuvo_script'),

    # Taboola page - Maya

    path('taboola_Maya/', views.taboola_Maya_page, name='taboola_Maya_page'),
    path('run_Maya_tonic_taboolaoffers_script/', views.run_Maya_tonic_taboolaoffers_script, name='run_Maya_tonic_taboolaoffers_script'),
    path('run_Maya_rsoctoniccreateofferestaboola_script/', views.run_Maya_rsoctoniccreateofferestaboola_script, name='run_Maya_rsoctoniccreateofferestaboola_script'),
    path('run_Maya_maxbidstaboola_UPCPCS1_script/', views.run_Maya_maxbidstaboola_UPCPCS1_script, name='run_Maya_maxbidstaboola_UPCPCS1_script'),
    path('run_Maya_maxbidstaboola_UPCPCRSOC_script/', views.run_Maya_maxbidstaboola_UPCPCRSOC_script, name='run_Maya_maxbidstaboola_UPCPCRSOC_script'),
    path('run_Maya_maxbidstaboola_UPCPC_script/', views.run_Maya_maxbidstaboola_UPCPC_script, name='run_Maya_maxbidstaboola_UPCPC_script'),
    path('run_Maya_maxbidstaboola_UPCPCINU_script/', views.run_Maya_maxbidstaboola_UPCPCINU_script, name='run_Maya_maxbidstaboola_UPCPCINU_script'),
    path('run_Maya_tabautooptshitty_script/', views.run_Maya_tabautooptshitty_script, name='run_Maya_tabautooptshitty_script'),
    path('run_Maya_tabautooptsourcestonic_script/', views.run_Maya_tabautooptsourcestonic_script, name='run_Maya_tabautooptsourcestonic_script'),

    path('run_Maya_tabduplicatorfortest_s1_script/', views.run_Maya_tabduplicatorfortest_s1_script, name='run_Maya_tabduplicatorfortest_s1_script'),
    path('run_Maya_tabduplicatorfortest_Inuvo_script/', views.run_Maya_tabduplicatorfortest_Inuvo_script, name='run_Maya_tabduplicatorfortest_Inuvo_script'),
    path('run_Maya_tabduplicatorfortest_AFD_script/', views.run_Maya_tabduplicatorfortest_AFD_script, name='run_Maya_tabduplicatorfortest_AFD_script'),
    path('run_Maya_tabduplicatorfortest_RSOC_script/', views.run_Maya_tabduplicatorfortest_RSOC_script, name='run_Maya_tabduplicatorfortest_RSOC_script'),
    path('run_Maya_tabduplicatorfortest_TC_script/', views.run_Maya_tabduplicatorfortest_TC_script, name='run_Maya_tabduplicatorfortest_TC_script'),


    path('run_Maya_upload_taboola_creatives_S1_script/', views.run_Maya_upload_taboola_creatives_S1_script, name='run_Maya_upload_taboola_creatives_S1_script'),
    path('run_Maya_upload_taboola_creatives_TC_script/', views.run_Maya_upload_taboola_creatives_TC_script, name='run_Maya_upload_taboola_creatives_TC_script'),
    path('run_Maya_upload_taboola_creatives_RSOC_script/', views.run_Maya_upload_taboola_creatives_RSOC_script, name='run_Maya_upload_taboola_creatives_RSOC_script'),
    path('run_Maya_upload_taboola_creatives_Inuvo_script/', views.run_Maya_upload_taboola_creatives_Inuvo_script, name='run_Maya_upload_taboola_creatives_Inuvo_script'),

    path('run_taboola_Maya_newpolicycheckforall_script/', views.run_taboola_Maya_newpolicycheckforall_script, name='run_taboola_Maya_newpolicycheckforall_script'),


    path('run_taboola_Maya__tchannels_createnew_script/', views.run_taboola_Maya__tchannels_createnew_script, name='run_taboola_Maya__tchannels_createnew_script'),
    path('run_taboola_Maya__tchannelsdb_script/', views.run_taboola_Maya__tchannelsdb_script, name='run_taboola_Maya__tchannelsdb_script'),



    # Taboola page - Dina

    path('taboola_Dina/', views.taboola_Dina_page, name='taboola_Dina_page'),
    path('run_Dina_tonic_taboolaoffers_script/', views.run_Dina_tonic_taboolaoffers_script, name='run_Dina_tonic_taboolaoffers_script'),
    path('run_Dina_rsoctoniccreateofferestaboola_script/', views.run_Dina_rsoctoniccreateofferestaboola_script, name='run_Dina_rsoctoniccreateofferestaboola_script'),
    path('run_Dina_maxbidstaboola_UPCPCS1_script/', views.run_Dina_maxbidstaboola_UPCPCS1_script, name='run_Dina_maxbidstaboola_UPCPCS1_script'),
    path('run_Dina_maxbidstaboola_UPCPCRSOC_script/', views.run_Dina_maxbidstaboola_UPCPCRSOC_script, name='run_Dina_maxbidstaboola_UPCPCRSOC_script'),
    path('run_Dina_maxbidstaboola_UPCPC_script/', views.run_Dina_maxbidstaboola_UPCPC_script, name='run_Dina_maxbidstaboola_UPCPC_script'),
    path('run_Dina_maxbidstaboola_UPCPCINU_script/', views.run_Dina_maxbidstaboola_UPCPCINU_script, name='run_Dina_maxbidstaboola_UPCPCINU_script'),

    path('run_Dina_tabduplicatorfortest_s1_script/', views.run_Dina_tabduplicatorfortest_s1_script, name='run_Dina_tabduplicatorfortest_s1_script'),
    path('run_Dina_tabduplicatorfortest_Inuvo_script/', views.run_Dina_tabduplicatorfortest_Inuvo_script, name='run_Dina_tabduplicatorfortest_Inuvo_script'),
    path('run_Dina_tabduplicatorfortest_AFD_script/', views.run_Dina_tabduplicatorfortest_AFD_script, name='run_Dina_tabduplicatorfortest_AFD_script'),
    path('run_Dina_tabduplicatorfortest_RSOC_script/', views.run_Dina_tabduplicatorfortest_RSOC_script, name='run_Dina_tabduplicatorfortest_RSOC_script'),
    path('run_Dina_tabduplicatorfortest_TC_script/', views.run_Dina_tabduplicatorfortest_TC_script, name='run_Dina_tabduplicatorfortest_TC_script'),

    path('run_taboola_Dina_newpolicycheckforall_script/', views.run_taboola_Dina_newpolicycheckforall_script, name='run_taboola_Dina_newpolicycheckforall_script'),


    path('run_taboola_Dina__tchannels_createnew_script/', views.run_taboola_Dina__tchannels_createnew_script, name='run_taboola_Dina__tchannels_createnew_script'),
    path('run_taboola_Dina__tchannelsdb_script/', views.run_taboola_Dina__tchannelsdb_script, name='run_taboola_Dina__tchannelsdb_script'),


    path('run_Dina_upload_taboola_creatives_S1_script/', views.run_Dina_upload_taboola_creatives_S1_script, name='run_Dina_upload_taboola_creatives_S1_script'),
    path('run_Dina_upload_taboola_creatives_TC_script/', views.run_Dina_upload_taboola_creatives_TC_script, name='run_Dina_upload_taboola_creatives_TC_script'),
    path('run_Dina_upload_taboola_creatives_RSOC_script/', views.run_Dina_upload_taboola_creatives_RSOC_script, name='run_Dina_upload_taboola_creatives_RSOC_script'),
    path('run_Dina_upload_taboola_creatives_Inuvo_script/', views.run_Dina_upload_taboola_creatives_Inuvo_script, name='run_Dina_upload_taboola_creatives_Inuvo_script'),



    # Taboola page - Or

    path('taboola_Or/', views.taboola_Or_page, name='taboola_Or_page'),
    path('run_Or_tonic_taboolaoffers_script/', views.run_Or_tonic_taboolaoffers_script, name='run_Or_tonic_taboolaoffers_script'),
    path('run_Or_rsoctoniccreateofferestaboola_script/', views.run_Or_rsoctoniccreateofferestaboola_script, name='run_Or_rsoctoniccreateofferestaboola_script'),
    path('run_Or_maxbidstaboola_UPCPCS1_script/', views.run_Or_maxbidstaboola_UPCPCS1_script, name='run_Or_maxbidstaboola_UPCPCS1_script'),
    path('run_Or_maxbidstaboola_UPCPCRSOC_script/', views.run_Or_maxbidstaboola_UPCPCRSOC_script, name='run_Or_maxbidstaboola_UPCPCRSOC_script'),
    path('run_Or_maxbidstaboola_UPCPC_script/', views.run_Or_maxbidstaboola_UPCPC_script, name='run_Or_maxbidstaboola_UPCPC_script'),
    path('run_Or_maxbidstaboola_UPCPCINU_script/', views.run_Or_maxbidstaboola_UPCPCINU_script, name='run_Or_maxbidstaboola_UPCPCINU_script'),

    path('run_Or_tabduplicatorfortest_s1_script/', views.run_Or_tabduplicatorfortest_s1_script, name='run_Or_tabduplicatorfortest_s1_script'),
    path('run_Or_tabduplicatorfortest_Inuvo_script/', views.run_Or_tabduplicatorfortest_Inuvo_script, name='run_Or_tabduplicatorfortest_Inuvo_script'),
    path('run_Or_tabduplicatorfortest_AFD_script/', views.run_Or_tabduplicatorfortest_AFD_script, name='run_Or_tabduplicatorfortest_AFD_script'),
    path('run_Or_tabduplicatorfortest_RSOC_script/', views.run_Or_tabduplicatorfortest_RSOC_script, name='run_Or_tabduplicatorfortest_RSOC_script'),
    path('run_Or_tabduplicatorfortest_TC_script/', views.run_Or_tabduplicatorfortest_TC_script, name='run_Or_tabduplicatorfortest_TC_script'),

    path('run_taboola_Or_newpolicycheckforall_script/', views.run_taboola_Or_newpolicycheckforall_script, name='run_taboola_Or_newpolicycheckforall_script'),

    path('run_taboola_Or__tchannels_createnew_script/', views.run_taboola_Or__tchannels_createnew_script, name='run_taboola_Or__tchannels_createnew_script'),
    path('run_taboola_Or__tchannelsdb_script/', views.run_taboola_Or__tchannelsdb_script, name='run_taboola_Or__tchannelsdb_script'),


    path('run_Or_upload_taboola_creatives_S1_script/', views.run_Or_upload_taboola_creatives_S1_script, name='run_Or_upload_taboola_creatives_S1_script'),
    path('run_Or_upload_taboola_creatives_TC_script/', views.run_Or_upload_taboola_creatives_TC_script, name='run_Or_upload_taboola_creatives_TC_script'),
    path('run_Or_upload_taboola_creatives_RSOC_script/', views.run_Or_upload_taboola_creatives_RSOC_script, name='run_Or_upload_taboola_creatives_RSOC_script'),
    path('run_Or_upload_taboola_creatives_Inuvo_script/', views.run_Or_upload_taboola_creatives_Inuvo_script, name='run_Or_upload_taboola_creatives_Inuvo_script'),



    # Taboola page - Yoav

    path('taboola_Yoav/', views.taboola_Yoav_page, name='taboola_Yoav_page'),
    path('run_Yoav_tonic_taboolaoffers_script/', views.run_Yoav_tonic_taboolaoffers_script, name='run_Yoav_tonic_taboolaoffers_script'),
    path('run_Yoav_rsoctoniccreateofferestaboola_script/', views.run_Yoav_rsoctoniccreateofferestaboola_script, name='run_Yoav_rsoctoniccreateofferestaboola_script'),
    path('run_Yoav_maxbidstaboola_UPCPCS1_script/', views.run_Yoav_maxbidstaboola_UPCPCS1_script, name='run_Yoav_maxbidstaboola_UPCPCS1_script'),
    path('run_Yoav_maxbidstaboola_UPCPCRSOC_script/', views.run_Yoav_maxbidstaboola_UPCPCRSOC_script, name='run_Yoav_maxbidstaboola_UPCPCRSOC_script'),
    path('run_Yoav_maxbidstaboola_UPCPC_script/', views.run_Yoav_maxbidstaboola_UPCPC_script, name='run_Yoav_maxbidstaboola_UPCPC_script'),
    path('run_Yoav_maxbidstaboola_UPCPCINU_script/', views.run_Yoav_maxbidstaboola_UPCPCINU_script, name='run_Yoav_maxbidstaboola_UPCPCINU_script'),

    path('run_Yoav_tabduplicatorfortest_s1_script/', views.run_Yoav_tabduplicatorfortest_s1_script, name='run_Yoav_tabduplicatorfortest_s1_script'),
    path('run_Yoav_tabduplicatorfortest_Inuvo_script/', views.run_Yoav_tabduplicatorfortest_Inuvo_script, name='run_Yoav_tabduplicatorfortest_Inuvo_script'),
    path('run_Yoav_tabduplicatorfortest_AFD_script/', views.run_Yoav_tabduplicatorfortest_AFD_script, name='run_Yoav_tabduplicatorfortest_AFD_script'),
    path('run_Yoav_tabduplicatorfortest_RSOC_script/', views.run_Yoav_tabduplicatorfortest_RSOC_script, name='run_Yoav_tabduplicatorfortest_RSOC_script'),
    path('run_Yoav_tabduplicatorfortest_TC_script/', views.run_Yoav_tabduplicatorfortest_TC_script, name='run_Yoav_tabduplicatorfortest_TC_script'),

    path('run_taboola_Yoav_newpolicycheckforall_script/', views.run_taboola_Yoav_newpolicycheckforall_script, name='run_taboola_Yoav_newpolicycheckforall_script'),
    path('run_Yoav_gcpgetdataforjenia_script/', views.run_Yoav_gcpgetdataforjenia_script, name='run_Yoav_gcpgetdataforjenia_script'),

    path('run_taboola_Yoav__tchannels_createnew_script/', views.run_taboola_Yoav__tchannels_createnew_script, name='run_taboola_Yoav__tchannels_createnew_script'),
    path('run_taboola_Yoav__tchannelsdb_script/', views.run_taboola_Yoav__tchannelsdb_script, name='run_taboola_Yoav__tchannelsdb_script'),


    path('run_Yoav_upload_taboola_creatives_S1_script/', views.run_Yoav_upload_taboola_creatives_S1_script, name='run_Yoav_upload_taboola_creatives_S1_script'),
    path('run_Yoav_upload_taboola_creatives_TC_script/', views.run_Yoav_upload_taboola_creatives_TC_script, name='run_Yoav_upload_taboola_creatives_TC_script'),
    path('run_Yoav_upload_taboola_creatives_RSOC_script/', views.run_Yoav_upload_taboola_creatives_RSOC_script, name='run_Yoav_upload_taboola_creatives_RSOC_script'),
    path('run_Yoav_upload_taboola_creatives_Inuvo_script/', views.run_Yoav_upload_taboola_creatives_Inuvo_script, name='run_Yoav_upload_taboola_creatives_Inuvo_script'),






    # Taboola page - Ilana

    path('taboola_Ilana/', views.taboola_Ilana_page, name='taboola_Ilana_page'),
    path('run_Ilana_tonic_taboolaoffers_script/', views.run_Ilana_tonic_taboolaoffers_script, name='run_Ilana_tonic_taboolaoffers_script'),
    path('run_Ilana_rsoctoniccreateofferestaboola_script/', views.run_Ilana_rsoctoniccreateofferestaboola_script, name='run_Ilana_rsoctoniccreateofferestaboola_script'),
    path('run_Ilana_maxbidstaboola_UPCPCS1_script/', views.run_Ilana_maxbidstaboola_UPCPCS1_script, name='run_Ilana_maxbidstaboola_UPCPCS1_script'),
    path('run_Ilana_maxbidstaboola_UPCPCRSOC_script/', views.run_Ilana_maxbidstaboola_UPCPCRSOC_script, name='run_Ilana_maxbidstaboola_UPCPCRSOC_script'),
    path('run_Ilana_maxbidstaboola_UPCPC_script/', views.run_Ilana_maxbidstaboola_UPCPC_script, name='run_Ilana_maxbidstaboola_UPCPC_script'),
    path('run_Ilana_maxbidstaboola_UPCPCINU_script/', views.run_Ilana_maxbidstaboola_UPCPCINU_script, name='run_Ilana_maxbidstaboola_UPCPCINU_script'),


    # Taboola page - Dor

    path('taboola_Dor/', views.taboola_Dor_page, name='taboola_Dor_page'),
    path('run_Dor_tonic_taboolaoffers_script/', views.run_Dor_tonic_taboolaoffers_script, name='run_Dor_tonic_taboolaoffers_script'),
    path('run_Dor_rsoctoniccreateofferestaboola_script/', views.run_Dor_rsoctoniccreateofferestaboola_script, name='run_Dor_rsoctoniccreateofferestaboola_script'),
    path('run_Dor_maxbidstaboola_UPCPCS1_script/', views.run_Dor_maxbidstaboola_UPCPCS1_script, name='run_Dor_maxbidstaboola_UPCPCS1_script'),
    path('run_Dor_maxbidstaboola_UPCPCRSOC_script/', views.run_Dor_maxbidstaboola_UPCPCRSOC_script, name='run_Dor_maxbidstaboola_UPCPCRSOC_script'),
    path('run_Dor_maxbidstaboola_UPCPC_script/', views.run_Dor_maxbidstaboola_UPCPC_script, name='run_Dor_maxbidstaboola_UPCPC_script'),
    path('run_Dor_maxbidstaboola_UPCPCINU_script/', views.run_Dor_maxbidstaboola_UPCPCINU_script, name='run_Dor_maxbidstaboola_UPCPCINU_script'),


    # Taboola page - Batel

    path('taboola_Batel/', views.taboola_Batel_page, name='taboola_Batel_page'),
    path('run_Batel_tonic_taboolaoffers_script/', views.run_Batel_tonic_taboolaoffers_script, name='run_Batel_tonic_taboolaoffers_script'),
    path('run_Batel_rsoctoniccreateofferestaboola_script/', views.run_Batel_rsoctoniccreateofferestaboola_script, name='run_Batel_rsoctoniccreateofferestaboola_script'),
    path('run_Batel_maxbidstaboola_UPCPCS1_script/', views.run_Batel_maxbidstaboola_UPCPCS1_script, name='run_Batel_maxbidstaboola_UPCPCS1_script'),
    path('run_Batel_maxbidstaboola_UPCPCRSOC_script/', views.run_Batel_maxbidstaboola_UPCPCRSOC_script, name='run_Batel_maxbidstaboola_UPCPCRSOC_script'),
    path('run_Batel_maxbidstaboola_UPCPC_script/', views.run_Batel_maxbidstaboola_UPCPC_script, name='run_Batel_maxbidstaboola_UPCPC_script'),
    path('run_Batel_maxbidstaboola_UPCPCINU_script/', views.run_Batel_maxbidstaboola_UPCPCINU_script, name='run_Batel_maxbidstaboola_UPCPCINU_script'),


    # Taboola page - Nofar

    path('taboola_Nofar/', views.taboola_Nofar_page, name='taboola_Nofar_page'),
    path('run_Nofar_tonic_taboolaoffers_script/', views.run_Nofar_tonic_taboolaoffers_script, name='run_Nofar_tonic_taboolaoffers_script'),
    path('run_Nofar_rsoctoniccreateofferestaboola_script/', views.run_Nofar_rsoctoniccreateofferestaboola_script, name='run_Nofar_rsoctoniccreateofferestaboola_script'),
    path('run_Nofar_maxbidstaboola_UPCPCS1_script/', views.run_Nofar_maxbidstaboola_UPCPCS1_script, name='run_Nofar_maxbidstaboola_UPCPCS1_script'),
    path('run_Nofar_maxbidstaboola_UPCPCRSOC_script/', views.run_Nofar_maxbidstaboola_UPCPCRSOC_script, name='run_Nofar_maxbidstaboola_UPCPCRSOC_script'),
    path('run_Nofar_maxbidstaboola_UPCPC_script/', views.run_Nofar_maxbidstaboola_UPCPC_script, name='run_Nofar_maxbidstaboola_UPCPC_script'),
    path('run_Nofar_maxbidstaboola_UPCPCINU_script/', views.run_Nofar_maxbidstaboola_UPCPCINU_script, name='run_Nofar_maxbidstaboola_UPCPCINU_script'),




################### Outbrain page

    # Outbrain page - Bulk

    path('outbrain_Bulk/', views.outbrain_Bulk_page, name='outbrain_Bulk_page'),
    path('run_Bulk_rsoctoniccreateofferesoutbrain_script/', views.run_Bulk_rsoctoniccreateofferesoutbrain_script, name='run_Bulk_rsoctoniccreateofferesoutbrain_script'),
    path('run_Bulk_tonic_outbrainoffers_script/', views.run_Bulk_tonic_outbrainoffers_script, name='run_Bulk_tonic_outbrainoffers_script'),

    path('run_KWCityCheckL_script/', views.run_KWCityCheckL_script, name='run_KWCityCheckL_script'),
    path('run_ShortenHeadlinesL_script/', views.run_ShortenHeadlinesL_script, name='run_ShortenHeadlinesL_script'),
    path('run_FKGOz2_script/', views.run_FKGOz2_script, name='run_FKGOz2_script'),

    path('run_outbrain_bulk_newpolicycheckforall_script/', views.run_outbrain_bulk_newpolicycheckforall_script, name='run_outbrain_bulk_newpolicycheckforall_script'),
    path('run_outbrain_bulk_gcpgetdataforjenia_script/', views.run_outbrain_bulk_gcpgetdataforjenia_script, name='run_outbrain_bulk_gcpgetdataforjenia_script'),


    path('run_outbrain_bulk__tchannels_createnew_script/', views.run_outbrain_bulk__tchannels_createnew_script, name='run_outbrain_bulk__tchannels_createnew_script'),
    path('run_outbrain_bulk__tchannelsdb_script/', views.run_outbrain_bulk__tchannelsdb_script, name='run_outbrain_bulk__tchannelsdb_script'),


    path('run_bulk_outbrain_uploader_script/', views.run_bulk_outbrain_uploader_script, name='run_bulk_outbrain_uploader_script'),


    # Outbrain page - Slavo

    path('outbrain_Slavo/', views.outbrain_Slavo_page, name='outbrain_Slavo_page'),
    path('run_Slavo_rsoctoniccreateofferesoutbrain_script/', views.run_Slavo_rsoctoniccreateofferesoutbrain_script, name='run_Slavo_rsoctoniccreateofferesoutbrain_script'),
    path('run_Slavo_tonic_outbrainoffers_script/', views.run_Slavo_tonic_outbrainoffers_script, name='run_Slavo_tonic_outbrainoffers_script'),

    path('run_outbrain_Slavo_newpolicycheckforall_script/', views.run_outbrain_Slavo_newpolicycheckforall_script, name='run_outbrain_Slavo_newpolicycheckforall_script'),
    path('run_Slavo_gcpgetdataforjenia_script/', views.run_Slavo_gcpgetdataforjenia_script, name='run_Slavo_gcpgetdataforjenia_script'),


    path('run_outbrain_Slavo__tchannels_createnew_script/', views.run_outbrain_Slavo__tchannels_createnew_script, name='run_outbrain_Slavo__tchannels_createnew_script'),
    path('run_outbrain_Slavo__tchannelsdb_script/', views.run_outbrain_Slavo__tchannelsdb_script, name='run_outbrain_Slavo__tchannelsdb_script'),


    # Outbrain page - Jelena

    path('outbrain_Jelena/', views.outbrain_Jelena_page, name='outbrain_Jelena_page'),
    path('run_Jelena_rsoctoniccreateofferesoutbrain_script/', views.run_Jelena_rsoctoniccreateofferesoutbrain_script, name='run_Jelena_rsoctoniccreateofferesoutbrain_script'),
    path('run_Jelena_tonic_outbrainoffers_script/', views.run_Jelena_tonic_outbrainoffers_script, name='run_Jelena_tonic_outbrainoffers_script'),

    path('run_outbrain_Jelena_newpolicycheckforall_script/', views.run_outbrain_Jelena_newpolicycheckforall_script, name='run_outbrain_Jelena_newpolicycheckforall_script'),
    path('run_Jelena_gcpgetdataforjenia_script/', views.run_Jelena_gcpgetdataforjenia_script, name='run_Jelena_gcpgetdataforjenia_script'),


    path('run_outbrain_Jelena__tchannels_createnew_script/', views.run_outbrain_Jelena__tchannels_createnew_script, name='run_outbrain_Jelena__tchannels_createnew_script'),
    path('run_outbrain_Jelena__tchannelsdb_script/', views.run_outbrain_Jelena__tchannelsdb_script, name='run_outbrain_Jelena__tchannelsdb_script'),

    # Outbrain page - Dimitrije

    path('outbrain_Dimitrije/', views.outbrain_Dimitrije_page, name='outbrain_Dimitrije_page'),
    path('run_Dimitrije_rsoctoniccreateofferesoutbrain_script/', views.run_Dimitrije_rsoctoniccreateofferesoutbrain_script, name='run_Dimitrije_rsoctoniccreateofferesoutbrain_script'),
    path('run_Dimitrije_tonic_outbrainoffers_script/', views.run_Dimitrije_tonic_outbrainoffers_script, name='run_Dimitrije_tonic_outbrainoffers_script'),

    path('run_outbrain_Dimitrije_newpolicycheckforall_script/', views.run_outbrain_Dimitrije_newpolicycheckforall_script, name='run_outbrain_Dimitrije_newpolicycheckforall_script'),
    path('run_Dimitrije_gcpgetdataforjenia_script/', views.run_Dimitrije_gcpgetdataforjenia_script, name='run_Dimitrije_gcpgetdataforjenia_script'),


    path('run_outbrain_Dimitrije__tchannels_createnew_script/', views.run_outbrain_Dimitrije__tchannels_createnew_script, name='run_outbrain_Dimitrije__tchannels_createnew_script'),
    path('run_outbrain_Dimitrije__tchannelsdb_script/', views.run_outbrain_Dimitrije__tchannelsdb_script, name='run_outbrain_Dimitrije__tchannelsdb_script'),


    # Outbrain page - Ivana_K

    path('outbrain_Ivana_K/', views.outbrain_Ivana_K_page, name='outbrain_Ivana_K_page'),
    path('run_Ivana_K_rsoctoniccreateofferesoutbrain_script/', views.run_Ivana_K_rsoctoniccreateofferesoutbrain_script, name='run_Ivana_K_rsoctoniccreateofferesoutbrain_script'),
    path('run_Ivana_K_tonic_outbrainoffers_script/', views.run_Ivana_K_tonic_outbrainoffers_script, name='run_Ivana_K_tonic_outbrainoffers_script'),

    path('run_outbrain_Ivana_K_newpolicycheckforall_script/', views.run_outbrain_Ivana_K_newpolicycheckforall_script, name='run_outbrain_Ivana_K_newpolicycheckforall_script'),
    path('run_Ivana_K_gcpgetdataforjenia_script/', views.run_Ivana_K_gcpgetdataforjenia_script, name='run_Ivana_K_gcpgetdataforjenia_script'),


    path('run_outbrain_Ivana_K__tchannels_createnew_script/', views.run_outbrain_Ivana_K__tchannels_createnew_script, name='run_outbrain_Ivana_K__tchannels_createnew_script'),
    path('run_outbrain_Ivana_K__tchannelsdb_script/', views.run_outbrain_Ivana_K__tchannelsdb_script, name='run_outbrain_Ivana_K__tchannelsdb_script'),


    # Outbrain page - Nemanja

    path('outbrain_Nemanja/', views.outbrain_Nemanja_page, name='outbrain_Nemanja_page'),
    path('run_Nemanja_rsoctoniccreateofferesoutbrain_script/', views.run_Nemanja_rsoctoniccreateofferesoutbrain_script, name='run_Nemanja_rsoctoniccreateofferesoutbrain_script'),
    path('run_Nemanja_tonic_outbrainoffers_script/', views.run_Nemanja_tonic_outbrainoffers_script, name='run_Nemanja_tonic_outbrainoffers_script'),

    path('run_outbrain_Nemanja_newpolicycheckforall_script/', views.run_outbrain_Nemanja_newpolicycheckforall_script, name='run_outbrain_Nemanja_newpolicycheckforall_script'),
    path('run_Nemanja_gcpgetdataforjenia_script/', views.run_Nemanja_gcpgetdataforjenia_script, name='run_Nemanja_gcpgetdataforjenia_script'),


    path('run_outbrain_Nemanja__tchannels_createnew_script/', views.run_outbrain_Nemanja__tchannels_createnew_script, name='run_outbrain_Nemanja__tchannels_createnew_script'),
    path('run_outbrain_Nemanja__tchannelsdb_script/', views.run_outbrain_Nemanja__tchannelsdb_script, name='run_outbrain_Nemanja__tchannelsdb_script'),





    # Outbrain page - Bartek

    path('outbrain_Bartek/', views.outbrain_Bartek_page, name='outbrain_Bartek_page'),
    path('run_Bartek_rsoctoniccreateofferesoutbrain_script/', views.run_Bartek_rsoctoniccreateofferesoutbrain_script, name='run_Bartek_rsoctoniccreateofferesoutbrain_script'),
    path('run_Bartek_tonic_outbrainoffers_script/', views.run_Bartek_tonic_outbrainoffers_script, name='run_Bartek_tonic_outbrainoffers_script'),


    # Outbrain page - Ivana_Z

    path('outbrain_Ivana_Z/', views.outbrain_Ivana_Z_page, name='outbrain_Ivana_Z_page'),
    path('run_Ivana_Z_rsoctoniccreateofferesoutbrain_script/', views.run_Ivana_Z_rsoctoniccreateofferesoutbrain_script, name='run_Ivana_Z_rsoctoniccreateofferesoutbrain_script'),
    path('run_Ivana_Z_tonic_outbrainoffers_script/', views.run_Ivana_Z_tonic_outbrainoffers_script, name='run_Ivana_Z_tonic_outbrainoffers_script'),


    # Outbrain page - Nadja

    path('outbrain_Nadja/', views.outbrain_Nadja_page, name='outbrain_Nadja_page'),
    path('run_Nadja_rsoctoniccreateofferesoutbrain_script/', views.run_Nadja_rsoctoniccreateofferesoutbrain_script, name='run_Nadja_rsoctoniccreateofferesoutbrain_script'),
    path('run_Nadja_tonic_outbrainoffers_script/', views.run_Nadja_tonic_outbrainoffers_script, name='run_Nadja_tonic_outbrainoffers_script'),



################### Zemanta page





    # Zemanta page - Bulk

    path('zemanta_Bulk/', views.zemanta_Bulk_page, name='zemanta_Bulk_page'),
    path('run_Bulk_rsoctoniccreateoffereszemanta_script/', views.run_Bulk_rsoctoniccreateoffereszemanta_script, name='run_Bulk_rsoctoniccreateoffereszemanta_script'),
    path('run_Bulk_tonic_zemantaoffers_script/', views.run_Bulk_tonic_zemantaoffers_script, name='run_Bulk_tonic_zemantaoffers_script'),



    ## image_cut


    path('run_Bulk_imagescutob_dup22_script/', views.run_Bulk_imagescutob_dup22_script, name='run_Bulk_imagescutob_dup22_script'),
    path('run_Bulk_imagescutob_dupinuvo_script/', views.run_Bulk_imagescutob_dupinuvo_script, name='run_Bulk_imagescutob_dupinuvo_script'),
    path('run_Bulk_imagescutob_duprsoc_script/', views.run_Bulk_imagescutob_duprsoc_script, name='run_Bulk_imagescutob_duprsoc_script'),
    path('run_Bulk_imagescutob_dups1_script/', views.run_Bulk_imagescutob_dups1_script, name='run_Bulk_imagescutob_dups1_script'),

    ##

    path('run_Bulk_ZemantaDescrip_script/', views.run_Bulk_ZemantaDescrip_script, name='run_Bulk_ZemantaDescrip_script'),
    path('run_Bulk_ZemantaShorthead_script/', views.run_Bulk_ZemantaShorthead_script, name='run_Bulk_ZemantaShorthead_script'),



    # Zemanta page - Bartek


    path('zemanta_Bartek/', views.zemanta_Bartek_page, name='zemanta_Bartek_page'),
    path('run_Bartek_rsoctoniccreateoffereszemanta_script/', views.run_Bartek_rsoctoniccreateoffereszemanta_script, name='run_Bartek_rsoctoniccreateoffereszemanta_script'),
    path('run_Bartek_tonic_zemantaoffers_script/', views.run_Bartek_tonic_zemantaoffers_script, name='run_Bartek_tonic_zemantaoffers_script'),


    ##image_cut


    path('run_Bartek_imagescutob_dup22_script/', views.run_Bartek_imagescutob_dup22_script, name='run_Bartek_imagescutob_dup22_script'),
    path('run_Bartek_imagescutob_dupinuvo_script/', views.run_Bartek_imagescutob_dupinuvo_script, name='run_Bartek_imagescutob_dupinuvo_script'),
    path('run_Bartek_imagescutob_duprsoc_script/', views.run_Bartek_imagescutob_duprsoc_script, name='run_Bartek_imagescutob_duprsoc_script'),
    path('run_Bartek_imagescutob_dups1_script/', views.run_Bartek_imagescutob_dups1_script, name='run_Bartek_imagescutob_dups1_script'),


    # Zemanta page - Nemanja

    path('zemanta_Nemanja/', views.zemanta_Nemanja_page, name='zemanta_Nemanja_page'),
    path('run_Nemanja_rsoctoniccreateoffereszemanta_script/', views.run_Nemanja_rsoctoniccreateoffereszemanta_script, name='run_Nemanja_rsoctoniccreateoffereszemanta_script'),
    path('run_Nemanja_tonic_zemantaoffers_script/', views.run_Nemanja_tonic_zemantaoffers_script, name='run_Nemanja_tonic_zemantaoffers_script'),


    ##image_cut


    path('run_Nemanja_imagescutob_dup22_script/', views.run_Nemanja_imagescutob_dup22_script, name='run_Nemanja_imagescutob_dup22_script'),
    path('run_Nemanja_imagescutob_dupinuvo_script/', views.run_Nemanja_imagescutob_dupinuvo_script, name='run_Nemanja_imagescutob_dupinuvo_script'),
    path('run_Nemanja_imagescutob_duprsoc_script/', views.run_Nemanja_imagescutob_duprsoc_script, name='run_Nemanja_imagescutob_duprsoc_script'),
    path('run_Nemanja_imagescutob_dups1_script/', views.run_Nemanja_imagescutob_dups1_script, name='run_Nemanja_imagescutob_dups1_script'),



    # Zemanta page - Petar

    path('zemanta_Petar/', views.zemanta_Petar_page, name='zemanta_Petar_page'),
    path('run_Petar_rsoctoniccreateoffereszemanta_script/', views.run_Petar_rsoctoniccreateoffereszemanta_script, name='run_Petar_rsoctoniccreateoffereszemanta_script'),
    path('run_Petar_tonic_zemantaoffers_script/', views.run_Petar_tonic_zemantaoffers_script, name='run_Petar_tonic_zemantaoffers_script'),


    ##image_cut


    path('run_Petar_imagescutob_dup22_script/', views.run_Petar_imagescutob_dup22_script, name='run_Petar_imagescutob_dup22_script'),
    path('run_Petar_imagescutob_dupinuvo_script/', views.run_Petar_imagescutob_dupinuvo_script, name='run_Petar_imagescutob_dupinuvo_script'),
    path('run_Petar_imagescutob_duprsoc_script/', views.run_Petar_imagescutob_duprsoc_script, name='run_Petar_imagescutob_duprsoc_script'),
    path('run_Petar_imagescutob_dups1_script/', views.run_Petar_imagescutob_dups1_script, name='run_Petar_imagescutob_dups1_script'),



    # Zemanta page - Dimitrije

    path('zemanta_Dimitrije/', views.zemanta_Dimitrije_page, name='zemanta_Dimitrije_page'),
    path('run_Dimitrije_rsoctoniccreateoffereszemanta_script/', views.run_Dimitrije_rsoctoniccreateoffereszemanta_script, name='run_Dimitrije_rsoctoniccreateoffereszemanta_script'),
    path('run_Dimitrije_tonic_zemantaoffers_script/', views.run_Dimitrije_tonic_zemantaoffers_script, name='run_Dimitrije_tonic_zemantaoffers_script'),


    ##image_cut


    path('run_Dimitrije_imagescutob_dup22_script/', views.run_Dimitrije_imagescutob_dup22_script, name='run_Dimitrije_imagescutob_dup22_script'),
    path('run_Dimitrije_imagescutob_dupinuvo_script/', views.run_Dimitrije_imagescutob_dupinuvo_script, name='run_Dimitrije_imagescutob_dupinuvo_script'),
    path('run_Dimitrije_imagescutob_duprsoc_script/', views.run_Dimitrije_imagescutob_duprsoc_script, name='run_Dimitrije_imagescutob_duprsoc_script'),
    path('run_Dimitrije_imagescutob_dups1_script/', views.run_Dimitrije_imagescutob_dups1_script, name='run_Dimitrije_imagescutob_dups1_script'),



    # Zemanta page - Nadja

    path('zemanta_Nadja/', views.zemanta_Nadja_page, name='zemanta_Nadja_page'),
    path('run_Nadja_rsoctoniccreateoffereszemanta_script/', views.run_Nadja_rsoctoniccreateoffereszemanta_script, name='run_Nadja_rsoctoniccreateoffereszemanta_script'),
    path('run_Nadja_tonic_zemantaoffers_script/', views.run_Nadja_tonic_zemantaoffers_script, name='run_Nadja_tonic_zemantaoffers_script'),


    ##image_cut


    path('run_Nadja_imagescutob_dup22_script/', views.run_Nadja_imagescutob_dup22_script, name='run_Nadja_imagescutob_dup22_script'),
    path('run_Nadja_imagescutob_dupinuvo_script/', views.run_Nadja_imagescutob_dupinuvo_script, name='run_Nadja_imagescutob_dupinuvo_script'),
    path('run_Nadja_imagescutob_duprsoc_script/', views.run_Nadja_imagescutob_duprsoc_script, name='run_Nadja_imagescutob_duprsoc_script'),
    path('run_Nadja_imagescutob_dups1_script/', views.run_Nadja_imagescutob_dups1_script, name='run_Nadja_imagescutob_dups1_script'),



    # Zemanta page - Slavo

    path('zemanta_Slavo/', views.zemanta_Slavo_page, name='zemanta_Slavo_page'),
    path('run_Slavo_rsoctoniccreateoffereszemanta_script/', views.run_Slavo_rsoctoniccreateoffereszemanta_script, name='run_Slavo_rsoctoniccreateoffereszemanta_script'),
    path('run_Slavo_tonic_zemantaoffers_script/', views.run_Slavo_tonic_zemantaoffers_script, name='run_Slavo_tonic_zemantaoffers_script'),


    ##image_cut


    path('run_Slavo_imagescutob_dup22_script/', views.run_Slavo_imagescutob_dup22_script, name='run_Slavo_imagescutob_dup22_script'),
    path('run_Slavo_imagescutob_dupinuvo_script/', views.run_Slavo_imagescutob_dupinuvo_script, name='run_Slavo_imagescutob_dupinuvo_script'),
    path('run_Slavo_imagescutob_duprsoc_script/', views.run_Slavo_imagescutob_duprsoc_script, name='run_Slavo_imagescutob_duprsoc_script'),
    path('run_Slavo_imagescutob_dups1_script/', views.run_Slavo_imagescutob_dups1_script, name='run_Slavo_imagescutob_dups1_script'),



    # Zemanta page - Ivana Z

    path('zemanta_Ivana_Z/', views.zemanta_Ivana_Z_page, name='zemanta_Ivana_Z_page'),
    path('run_Ivana_Z_rsoctoniccreateoffereszemanta_script/', views.run_Ivana_Z_rsoctoniccreateoffereszemanta_script, name='run_Ivana_Z_rsoctoniccreateoffereszemanta_script'),
    path('run_Ivana_Z_tonic_zemantaoffers_script/', views.run_Ivana_Z_tonic_zemantaoffers_script, name='run_Ivana_Z_tonic_zemantaoffers_script'),


    ##image_cut


    path('run_Ivana_Z_imagescutob_dup22_script/', views.run_Ivana_Z_imagescutob_dup22_script, name='run_Ivana_Z_imagescutob_dup22_script'),
    path('run_Ivana_Z_imagescutob_dupinuvo_script/', views.run_Ivana_Z_imagescutob_dupinuvo_script, name='run_Ivana_Z_imagescutob_dupinuvo_script'),
    path('run_Ivana_Z_imagescutob_duprsoc_script/', views.run_Ivana_Z_imagescutob_duprsoc_script, name='run_Ivana_Z_imagescutob_duprsoc_script'),
    path('run_Ivana_Z_imagescutob_dups1_script/', views.run_Ivana_Z_imagescutob_dups1_script, name='run_Ivana_Z_imagescutob_dups1_script'),



    # Zemanta page - Jelena

    path('zemanta_Jelena/', views.zemanta_Jelena_page, name='zemanta_Jelena_page'),
    path('run_Jelena_rsoctoniccreateoffereszemanta_script/', views.run_Jelena_rsoctoniccreateoffereszemanta_script, name='run_Jelena_rsoctoniccreateoffereszemanta_script'),
    path('run_Jelena_tonic_zemantaoffers_script/', views.run_Jelena_tonic_zemantaoffers_script, name='run_Jelena_tonic_zemantaoffers_script'),


    ##image_cut


    path('run_Jelena_imagescutob_dup22_script/', views.run_Jelena_imagescutob_dup22_script, name='run_Jelena_imagescutob_dup22_script'),
    path('run_Jelena_imagescutob_dupinuvo_script/', views.run_Jelena_imagescutob_dupinuvo_script, name='run_Jelena_imagescutob_dupinuvo_script'),
    path('run_Jelena_imagescutob_duprsoc_script/', views.run_Jelena_imagescutob_duprsoc_script, name='run_Jelena_imagescutob_duprsoc_script'),
    path('run_Jelena_imagescutob_dups1_script/', views.run_Jelena_imagescutob_dups1_script, name='run_Jelena_imagescutob_dups1_script'),



    # Zemanta page - Ivana K

    path('zemanta_Ivana_K/', views.zemanta_Ivana_K_page, name='zemanta_Ivana_K_page'),
    path('run_Ivana_K_rsoctoniccreateoffereszemanta_script/', views.run_Ivana_K_rsoctoniccreateoffereszemanta_script, name='run_Ivana_K_rsoctoniccreateoffereszemanta_script'),
    path('run_Ivana_K_tonic_zemantaoffers_script/', views.run_Ivana_K_tonic_zemantaoffers_script, name='run_Ivana_K_tonic_zemantaoffers_script'),


    ##image_cut


    path('run_Ivana_K_imagescutob_dup22_script/', views.run_Ivana_K_imagescutob_dup22_script, name='run_Ivana_K_imagescutob_dup22_script'),
    path('run_Ivana_K_imagescutob_dupinuvo_script/', views.run_Ivana_K_imagescutob_dupinuvo_script, name='run_Ivana_K_imagescutob_dupinuvo_script'),
    path('run_Ivana_K_imagescutob_duprsoc_script/', views.run_Ivana_K_imagescutob_duprsoc_script, name='run_Ivana_K_imagescutob_duprsoc_script'),
    path('run_Ivana_K_imagescutob_dups1_script/', views.run_Ivana_K_imagescutob_dups1_script, name='run_Ivana_K_imagescutob_dups1_script'),






################### Google page





    # Google page - Bulk



    path('google_Bulk/', views.google_Bulk_page, name='google_Bulk_page'),
    path('run_Bulk_Manual_imagescut_script/', views.run_Bulk_Manual_imagescut_script, name='run_Bulk_Manual_imagescut_script'),
    path('run_Bulk_GoogleCreateve_IMG_script/', views.run_Bulk_GoogleCreateve_IMG_script, name='run_Bulk_GoogleCreateve_IMG_script'),
    path('run_Bulk_GoogleCreateve_IMG_Split_script/', views.run_Bulk_GoogleCreateve_IMG_Split_script, name='run_Bulk_GoogleCreateve_IMG_Split_script'),
    path('run_Bulk_GoogleGPTCreative_step1_script/', views.run_Bulk_GoogleGPTCreative_step1_script, name='run_Bulk_GoogleGPTCreative_step1_script'),
    path('run_Bulk_GoogleGPTCreative_step2_script/', views.run_Bulk_GoogleGPTCreative_step2_script, name='run_Bulk_GoogleGPTCreative_step2_script'),

    path('run_Bulk_GoogleRSoCTonicActiveLinks_script/', views.run_Bulk_GoogleRSoCTonicActiveLinks_script, name='run_Bulk_GoogleRSoCTonicActiveLinks_script'),
    path('run_Bulk_GoogleRSoCTonicCreatLinks_script/', views.run_Bulk_GoogleRSoCTonicCreatLinks_script, name='run_Bulk_GoogleRSoCTonicCreatLinks_script'),


    path('run_google_bulk__tchannels_createnew_script/', views.run_google_bulk__tchannels_createnew_script, name='run_google_bulk__tchannels_createnew_script'),
    path('run_google_bulk__tchannelsdb_script/', views.run_google_bulk__tchannelsdb_script, name='run_google_bulk__tchannelsdb_script'),


    path('run_google_bulk_newpolicycheckforall_script/', views.run_google_bulk_newpolicycheckforall_script, name='run_google_bulk_newpolicycheckforall_script'),


    path('run_Bulk_google_uploader_v3_script/', views.run_Bulk_google_uploader_v3_script, name='run_Bulk_google_uploader_v3_script'),
    path('run_Bulk_google_uploader_v3_image_test_script/', views.run_Bulk_google_uploader_v3_image_test_script, name='run_Bulk_google_uploader_v3_image_test_script'),


    # Google page - Maya



    path('google_Maya/', views.google_Maya_page, name='google_Maya_page'),
    path('run_Maya_Manual_imagescut_script/', views.run_Maya_Manual_imagescut_script, name='run_Maya_Manual_imagescut_script'),
    path('run_Maya_GoogleCreateve_IMG_script/', views.run_Maya_GoogleCreateve_IMG_script, name='run_Maya_GoogleCreateve_IMG_script'),
    path('run_Maya_GoogleCreateve_IMG_Split_script/', views.run_Maya_GoogleCreateve_IMG_Split_script, name='run_Maya_GoogleCreateve_IMG_Split_script'),
    path('run_Maya_GoogleGPTCreative_step1_script/', views.run_Maya_GoogleGPTCreative_step1_script, name='run_Maya_GoogleGPTCreative_step1_script'),
    path('run_Maya_GoogleGPTCreative_step2_script/', views.run_Maya_GoogleGPTCreative_step2_script, name='run_Maya_GoogleGPTCreative_step2_script'),

    path('run_Maya_GoogleRSoCTonicActiveLinks_script/', views.run_Maya_GoogleRSoCTonicActiveLinks_script, name='run_Maya_GoogleRSoCTonicActiveLinks_script'),
    path('run_Maya_GoogleRSoCTonicCreatLinks_script/', views.run_Maya_GoogleRSoCTonicCreatLinks_script, name='run_Maya_GoogleRSoCTonicCreatLinks_script'),

    path('run_google_Maya_newpolicycheckforall_script/', views.run_google_Maya_newpolicycheckforall_script, name='run_google_Maya_newpolicycheckforall_script'),
    path('run_Maya_newpolicycheckforall_script/', views.run_Maya_newpolicycheckforall_script, name='run_Maya_newpolicycheckforall_script'),
    path('run_Maya_gcpgetdataforjenia_script/', views.run_Maya_gcpgetdataforjenia_script, name='run_Maya_gcpgetdataforjenia_script'),


    path('run_google_Maya__tchannelsdb_script/', views.run_google_Maya__tchannelsdb_script, name='run_google_Maya__tchannelsdb_script'),
    path('run_google_Maya__tchannels_createnew_script/', views.run_google_Maya__tchannels_createnew_script, name='run_google_Maya__tchannels_createnew_script'),


    path('run_Maya_google_uploader_v3_image_test_script/', views.run_Maya_google_uploader_v3_image_test_script, name='run_Maya_google_uploader_v3_image_test_script'),


    # Google page - Or



    path('google_Or/', views.google_Or_page, name='google_Or_page'),
    path('run_Or_Manual_imagescut_script/', views.run_Or_Manual_imagescut_script, name='run_Or_Manual_imagescut_script'),
    path('run_Or_Creative_imagescut_script/', views.run_Or_Creative_imagescut_script, name='run_Or_Creative_imagescut_script'),

    path('run_Or_google_uploader_v3_script/', views.run_Or_google_uploader_v3_script, name='run_Or_google_uploader_v3_script'),

    path('run_Or_GoogleRSoCTonicActiveLinks_script/', views.run_Or_GoogleRSoCTonicActiveLinks_script, name='run_Or_GoogleRSoCTonicActiveLinks_script'),
    path('run_Or_GoogleRSoCTonicCreatLinks_script/', views.run_Or_GoogleRSoCTonicCreatLinks_script, name='run_Or_GoogleRSoCTonicCreatLinks_script'),

    path('run_google_Or_newpolicycheckforall_script/', views.run_google_Or_newpolicycheckforall_script, name='run_google_Or_newpolicycheckforall_script'),
    path('run_Or_newpolicycheckforall_script/', views.run_Or_newpolicycheckforall_script, name='run_Or_newpolicycheckforall_script'),
    path('run_Or_gcpgetdataforjenia_script/', views.run_Or_gcpgetdataforjenia_script, name='run_Or_gcpgetdataforjenia_script'),


    path('run_google_Or__tchannels_createnew_script/', views.run_google_Or__tchannels_createnew_script, name='run_google_Or__tchannels_createnew_script'),
    path('run_google_Or__tchannelsdb_script/', views.run_google_Or__tchannelsdb_script, name='run_google_Or__tchannelsdb_script'),



    # Google page - Dina

    path('google_Dina/', views.google_Dina_page, name='google_Dina_page'),
    path('run_Dina_Manual_imagescut_script/', views.run_Dina_Manual_imagescut_script, name='run_Dina_Manual_imagescut_script'),
    path('run_Dina_Creative_imagescut_script/', views.run_Dina_Creative_imagescut_script, name='run_Dina_Creative_imagescut_script'),

    path('run_Dina_google_uploader_v3_script/', views.run_Dina_google_uploader_v3_script, name='run_Dina_google_uploader_v3_script'),

    path('run_Dina_GoogleRSoCTonicActiveLinks_script/', views.run_Dina_GoogleRSoCTonicActiveLinks_script, name='run_Dina_GoogleRSoCTonicActiveLinks_script'),
    path('run_Dina_GoogleRSoCTonicCreatLinks_script/', views.run_Dina_GoogleRSoCTonicCreatLinks_script, name='run_Dina_GoogleRSoCTonicCreatLinks_script'),

    path('run_google_Dina_newpolicycheckforall_script/', views.run_google_Dina_newpolicycheckforall_script, name='run_google_Dina_newpolicycheckforall_script'),
    path('run_Dina_newpolicycheckforall_script/', views.run_Dina_newpolicycheckforall_script, name='run_Dina_newpolicycheckforall_script'),
    path('run_Dina_gcpgetdataforjenia_script/', views.run_Dina_gcpgetdataforjenia_script, name='run_Dina_gcpgetdataforjenia_script'),


    path('run_google_Dina__tchannels_createnew_script/', views.run_google_Dina__tchannels_createnew_script, name='run_google_Dina__tchannels_createnew_script'),
    path('run_google_Dina__tchannelsdb_script/', views.run_google_Dina__tchannelsdb_script, name='run_google_Dina__tchannelsdb_script'),




    # Google page - Yoav



    path('google_Yoav/', views.google_Yoav_page, name='google_Yoav_page'),
    path('run_Yoav_Manual_imagescut_script/', views.run_Yoav_Manual_imagescut_script, name='run_Yoav_Manual_imagescut_script'),
    path('run_Yoav_Creative_imagescut_script/', views.run_Yoav_Creative_imagescut_script, name='run_Yoav_Creative_imagescut_script'),

    path('run_Yoav_google_uploader_v3_script/', views.run_Yoav_google_uploader_v3_script, name='run_Yoav_google_uploader_v3_script'),

    path('run_Yoav_GoogleRSoCTonicActiveLinks_script/', views.run_Yoav_GoogleRSoCTonicActiveLinks_script, name='run_Yoav_GoogleRSoCTonicActiveLinks_script'),
    path('run_Yoav_GoogleRSoCTonicCreatLinks_script/', views.run_Yoav_GoogleRSoCTonicCreatLinks_script, name='run_Yoav_GoogleRSoCTonicCreatLinks_script'),

    path('run_google_Yoav_newpolicycheckforall_script/', views.run_google_Yoav_newpolicycheckforall_script, name='run_google_Yoav_newpolicycheckforall_script'),
    path('run_Yoav_newpolicycheckforall_script/', views.run_Yoav_newpolicycheckforall_script, name='run_Yoav_newpolicycheckforall_script'),
    path('run_Yoav_gcpgetdataforjenia_script/', views.run_Yoav_gcpgetdataforjenia_script, name='run_Yoav_gcpgetdataforjenia_script'),


    path('run_google_Yoav__tchannels_createnew_script/', views.run_google_Yoav__tchannels_createnew_script, name='run_google_Yoav__tchannels_createnew_script'),
    path('run_google_Yoav__tchannelsdb_script/', views.run_google_Yoav__tchannelsdb_script, name='run_google_Yoav__tchannelsdb_script'),


    # Google page - Elad



    path('google_Elad/', views.google_Elad_page, name='google_Elad_page'),

    path('run_Elad_Manual_imagescut_script/', views.run_Elad_Manual_imagescut_script, name='run_Elad_Manual_imagescut_script'),
    path('run_Elad_Creative_imagescut_script/', views.run_Elad_Creative_imagescut_script, name='run_Elad_Creative_imagescut_script'),

    path('run_Elad_google_uploader_v3_script/', views.run_Elad_google_uploader_v3_script, name='run_Elad_google_uploader_v3_script'),


    path('run_Elad_GoogleRSoCTonicActiveLinks_script/', views.run_Elad_GoogleRSoCTonicActiveLinks_script, name='run_Elad_GoogleRSoCTonicActiveLinks_script'),
    path('run_Elad_GoogleRSoCTonicCreatLinks_script/', views.run_Elad_GoogleRSoCTonicCreatLinks_script, name='run_Elad_GoogleRSoCTonicCreatLinks_script'),

    path('run_google_Elad_newpolicycheckforall_script/', views.run_google_Elad_newpolicycheckforall_script, name='run_google_Elad_newpolicycheckforall_script'),
    path('run_Elad_newpolicycheckforall_script/', views.run_Elad_newpolicycheckforall_script, name='run_Elad_newpolicycheckforall_script'),
    path('run_Elad_gcpgetdataforjenia_script/', views.run_Elad_gcpgetdataforjenia_script, name='run_Elad_gcpgetdataforjenia_script'),

    path('run_google_Elad__tchannelsdb_script/', views.run_google_Elad__tchannelsdb_script, name='run_google_Elad__tchannelsdb_script'),
    path('run_google_Elad__tchannels_createnew_script/', views.run_google_Elad__tchannels_createnew_script, name='run_google_Elad__tchannels_createnew_script'),




    # Google page - Elran




    path('google_Elran/', views.google_Elran_page, name='google_Elran_page'),
    path('run_Elran_Manual_imagescut_script/', views.run_Elran_Manual_imagescut_script, name='run_Elran_Manual_imagescut_script'),
    path('run_Elran_Creative_imagescut_script/', views.run_Elran_Creative_imagescut_script, name='run_Elran_Creative_imagescut_script'),

    path('run_Elran_google_uploader_v3_script/', views.run_Elran_google_uploader_v3_script, name='run_Elran_google_uploader_v3_script'),

    path('run_Elran_GoogleRSoCTonicActiveLinks_script/', views.run_Elran_GoogleRSoCTonicActiveLinks_script, name='run_Elran_GoogleRSoCTonicActiveLinks_script'),
    path('run_Elran_GoogleRSoCTonicCreatLinks_script/', views.run_Elran_GoogleRSoCTonicCreatLinks_script, name='run_Elran_GoogleRSoCTonicCreatLinks_script'),

    path('run_google_Elran_newpolicycheckforall_script/', views.run_google_Elran_newpolicycheckforall_script, name='run_google_Elran_newpolicycheckforall_script'),
    path('run_Elran_newpolicycheckforall_script/', views.run_Elran_newpolicycheckforall_script, name='run_Elran_newpolicycheckforall_script'),
    path('run_Elran_gcpgetdataforjenia_script/', views.run_Elran_gcpgetdataforjenia_script, name='run_Elran_gcpgetdataforjenia_script'),


    path('run_google_Elran__tchannels_createnew_script/', views.run_google_Elran__tchannels_createnew_script, name='run_google_Elran__tchannels_createnew_script'),
    path('run_google_Elran__tchannelsdb_script/', views.run_google_Elran__tchannelsdb_script, name='run_google_Elran__tchannelsdb_script'),




    # Google page - Omer



    path('google_Omer/', views.google_Omer_page, name='google_Omer_page'),
    path('run_Omer_Manual_imagescut_script/', views.run_Omer_Manual_imagescut_script, name='run_Omer_Manual_imagescut_script'),
    path('run_Omer_Creative_imagescut_script/', views.run_Omer_Creative_imagescut_script, name='run_Omer_Creative_imagescut_script'),

    path('run_Omer_GoogleRSoCTonicActiveLinks_script/', views.run_Omer_GoogleRSoCTonicActiveLinks_script, name='run_Omer_GoogleRSoCTonicActiveLinks_script'),
    path('run_Omer_GoogleRSoCTonicCreatLinks_script/', views.run_Omer_GoogleRSoCTonicCreatLinks_script, name='run_Omer_GoogleRSoCTonicCreatLinks_script'),

    path('run_google_Omer_newpolicycheckforall_script/', views.run_google_Omer_newpolicycheckforall_script, name='run_google_Omer_newpolicycheckforall_script'),
    path('run_Omer_newpolicycheckforall_script/', views.run_Omer_newpolicycheckforall_script, name='run_Omer_newpolicycheckforall_script'),

    path('run_google_Omer__tchannels_createnew_script/', views.run_google_Omer__tchannels_createnew_script, name='run_google_Omer__tchannels_createnew_script'),
    path('run_google_Omer__tchannelsdb_script/', views.run_google_Omer__tchannelsdb_script, name='run_google_Omer__tchannelsdb_script'),



################### Poppin page



    # Poppin page - Bulk



    path('run_Poppin_bulk__tchannels_createnew_script/', views.run_Poppin_bulk__tchannels_createnew_script, name='run_Poppin_bulk__tchannels_createnew_script'),
    path('run_Poppin_bulk__tchannelsdb_script/', views.run_Poppin_bulk__tchannelsdb_script, name='run_Poppin_bulk__tchannelsdb_script'),



    # poppin page - Elad

    path('poppin_Elad/', views.poppin_Elad_page, name='poppin_Elad_page'),
    path('run_Elad_rsoctoniccreateofferspoppin_script/', views.run_Elad_rsoctoniccreateofferspoppin_script, name='run_Elad_rsoctoniccreateofferspoppin_script'),
    path('run_Elad_tonic_poppinoffers_script/', views.run_Elad_tonic_poppinoffers_script, name='run_Elad_tonic_poppinoffers_script'),


    path('run_Poppin_Elad__tchannels_createnew_script/', views.run_Poppin_Elad__tchannels_createnew_script, name='run_Poppin_Elad__tchannels_createnew_script'),
    path('run_Poppin_Elad__tchannelsdb_script/', views.run_Poppin_Elad__tchannelsdb_script, name='run_Poppin_Elad__tchannelsdb_script'),



    # poppin page - Matan

    path('poppin_Matan/', views.poppin_Matan_page, name='poppin_Matan_page'),
    path('run_Matan_rsoctoniccreateofferspoppin_script/', views.run_Matan_rsoctoniccreateofferspoppin_script, name='run_Matan_rsoctoniccreateofferspoppin_script'),
    path('run_Matan_tonic_poppinoffers_script/', views.run_Matan_tonic_poppinoffers_script, name='run_Matan_tonic_poppinoffers_script'),


    path('run_Poppin_Matan__tchannels_createnew_script/', views.run_Poppin_Matan__tchannels_createnew_script, name='run_Poppin_Matan__tchannels_createnew_script'),
    path('run_Poppin_Matan__tchannelsdb_script/', views.run_Poppin_Matan__tchannelsdb_script, name='run_Poppin_Matan__tchannelsdb_script'),






################### Facebook page





    # Facebook page - Bulk

    path('facebook_Bulk/', views.facebook_Bulk_page, name='facebook_Bulk_page'),
    path('run_Bulk_FBRSoCTonicCreatLinks_script/', views.run_Bulk_FBRSoCTonicCreatLinks_script, name='run_Bulk_FBRSoCTonicCreatLinks_script'),
    path('run_Bulk_tonic_FBoffers_script/', views.run_Bulk_tonic_FBoffers_script, name='run_Bulk_tonic_FBoffers_script'),
    path('run_Bulk_FBRSoCTonicCreatpixel_script/', views.run_Bulk_FBRSoCTonicCreatpixel_script, name='run_Bulk_FBRSoCTonicCreatpixel_script'),
    path('run_Bulk_FBRSoCTonicCreat_link_pixel_script/', views.run_Bulk_FBRSoCTonicCreat_link_pixel_script, name='run_Bulk_FBRSoCTonicCreat_link_pixel_script'),


    path('run_Bulk_predictochannels_createnew_script/', views.run_Bulk_predictochannels_createnew_script, name='run_Bulk_predictochannels_createnew_script'),
    path('run_Bulk_Compadochannels_createnew_script/', views.run_Bulk_Compadochannels_createnew_script, name='run_Bulk_Compadochannels_createnew_script'),
    path('run_Bulk_predictochannelsdb_script/', views.run_Bulk_predictochannelsdb_script, name='run_Bulk_predictochannelsdb_script'),


    path('run_facebook_Bulk_tc_channels_createnew_script/', views.run_facebook_Bulk_tc_channels_createnew_script, name='run_facebook_Bulk_tc_channels_createnew_script'),
    path('run_facebook_Bulk_tc_channelsdb_script/', views.run_facebook_Bulk_tc_channelsdb_script, name='run_facebook_Bulk_tc_channelsdb_script'),


    path('run_facebook_Bulk_newpolicycheckforall_script/', views.run_facebook_Bulk_newpolicycheckforall_script, name='run_facebook_Bulk_newpolicycheckforall_script'),

    path('run_facebook_Bulk_Extract_TXT_IMG_script/', views.run_facebook_Bulk_Extract_TXT_IMG_script, name='run_facebook_Bulk_Extract_TXT_IMG_script'),

    path('run_Bulk_fb_uploader_v26_script/', views.run_Bulk_fb_uploader_v26_script, name='run_Bulk_fb_uploader_v26_script'),

    # Facebook page - Andrea

    path('facebook_Andrea/', views.facebook_Andrea_page, name='facebook_Andrea_page'),
    path('run_Andrea_FBRSoCTonicCreatLinks_script/', views.run_Andrea_FBRSoCTonicCreatLinks_script, name='run_Andrea_FBRSoCTonicCreatLinks_script'),
    path('run_Andrea_tonic_FBoffers_script/', views.run_Andrea_tonic_FBoffers_script, name='run_Andrea_tonic_FBoffers_script'),
    path('run_Andrea_FBRSoCTonicCreatpixel_script/', views.run_Andrea_FBRSoCTonicCreatpixel_script, name='run_Andrea_FBRSoCTonicCreatpixel_script'),
    path('run_Andrea_FBRSoCTonicCreat_link_pixel_script/', views.run_Andrea_FBRSoCTonicCreat_link_pixel_script, name='run_Andrea_FBRSoCTonicCreat_link_pixel_script'),

    path('run_Andrea_predictochannels_createnew_script/', views.run_Andrea_predictochannels_createnew_script, name='run_Andrea_predictochannels_createnew_script'),
    path('run_Andrea_Compadochannels_createnew_script/', views.run_Andrea_Compadochannels_createnew_script, name='run_Andrea_Compadochannels_createnew_script'),
    path('run_Andrea_predictochannelsdb_script/', views.run_Andrea_predictochannelsdb_script, name='run_Andrea_predictochannelsdb_script'),

    path('run_facebook_Andrea_Extract_TXT_IMG_script/', views.run_facebook_Andrea_Extract_TXT_IMG_script, name='run_facebook_Andrea_Extract_TXT_IMG_script'),


    # Facebook page - Slavo

    path('facebook_Slavo/', views.facebook_Slavo_page, name='facebook_Slavo_page'),
    path('run_Slavo_FBRSoCTonicCreatLinks_script/', views.run_Slavo_FBRSoCTonicCreatLinks_script, name='run_Slavo_FBRSoCTonicCreatLinks_script'),
    path('run_Slavo_tonic_FBoffers_script/', views.run_Slavo_tonic_FBoffers_script, name='run_Slavo_tonic_FBoffers_script'),
    path('run_Slavo_FBRSoCTonicCreatpixel_script/', views.run_Slavo_FBRSoCTonicCreatpixel_script, name='run_Slavo_FBRSoCTonicCreatpixel_script'),
    path('run_Slavo_FBRSoCTonicCreat_link_pixel_script/', views.run_Slavo_FBRSoCTonicCreat_link_pixel_script, name='run_Slavo_FBRSoCTonicCreat_link_pixel_script'),


    path('run_Slavo_predictochannels_createnew_script/', views.run_Slavo_predictochannels_createnew_script, name='run_Slavo_predictochannels_createnew_script'),
    path('run_Slavo_Compadochannels_createnew_script/', views.run_Slavo_Compadochannels_createnew_script, name='run_Slavo_Compadochannels_createnew_script'),
    path('run_Slavo_predictochannelsdb_script/', views.run_Slavo_predictochannelsdb_script, name='run_Slavo_predictochannelsdb_script'),

    path('run_facebook_Slavo_Extract_TXT_IMG_script/', views.run_facebook_Slavo_Extract_TXT_IMG_script, name='run_facebook_Slavo_Extract_TXT_IMG_script'),


    # Facebook page - Jelena

    path('facebook_Jelena/', views.facebook_Jelena_page, name='facebook_Jelena_page'),
    path('run_Jelena_FBRSoCTonicCreatLinks_script/', views.run_Jelena_FBRSoCTonicCreatLinks_script, name='run_Jelena_FBRSoCTonicCreatLinks_script'),
    path('run_Jelena_tonic_FBoffers_script/', views.run_Jelena_tonic_FBoffers_script, name='run_Jelena_tonic_FBoffers_script'),
    path('run_Jelena_FBRSoCTonicCreatpixel_script/', views.run_Jelena_FBRSoCTonicCreatpixel_script, name='run_Jelena_FBRSoCTonicCreatpixel_script'),
    path('run_Jelena_FBRSoCTonicCreat_link_pixel_script/', views.run_Jelena_FBRSoCTonicCreat_link_pixel_script, name='run_Jelena_FBRSoCTonicCreat_link_pixel_script'),


    path('run_Jelena_predictochannels_createnew_script/', views.run_Jelena_predictochannels_createnew_script, name='run_Jelena_predictochannels_createnew_script'),
    path('run_Jelena_Compadochannels_createnew_script/', views.run_Jelena_Compadochannels_createnew_script, name='run_Jelena_Compadochannels_createnew_script'),
    path('run_Jelena_predictochannelsdb_script/', views.run_Jelena_predictochannelsdb_script, name='run_Jelena_predictochannelsdb_script'),

    path('run_facebook_Jelena_Extract_TXT_IMG_script/', views.run_facebook_Jelena_Extract_TXT_IMG_script, name='run_facebook_Jelena_Extract_TXT_IMG_script'),


    # Facebook page - Dimitrije

    path('facebook_Dimitrije/', views.facebook_Dimitrije_page, name='facebook_Dimitrije_page'),
    path('run_Dimitrije_FBRSoCTonicCreatLinks_script/', views.run_Dimitrije_FBRSoCTonicCreatLinks_script, name='run_Dimitrije_FBRSoCTonicCreatLinks_script'),
    path('run_Dimitrije_tonic_FBoffers_script/', views.run_Dimitrije_tonic_FBoffers_script, name='run_Dimitrije_tonic_FBoffers_script'),
    path('run_Dimitrije_FBRSoCTonicCreatpixel_script/', views.run_Dimitrije_FBRSoCTonicCreatpixel_script, name='run_Dimitrije_FBRSoCTonicCreatpixel_script'),
    path('run_Dimitrije_FBRSoCTonicCreat_link_pixel_script/', views.run_Dimitrije_FBRSoCTonicCreat_link_pixel_script, name='run_Dimitrije_FBRSoCTonicCreat_link_pixel_script'),

    path('run_Dimitrije_predictochannels_createnew_script/', views.run_Dimitrije_predictochannels_createnew_script, name='run_Dimitrije_predictochannels_createnew_script'),
    path('run_Dimitrije_Compadochannels_createnew_script/', views.run_Dimitrije_Compadochannels_createnew_script, name='run_Dimitrije_Compadochannels_createnew_script'),
    path('run_Dimitrije_predictochannelsdb_script/', views.run_Dimitrije_predictochannelsdb_script, name='run_Dimitrije_predictochannelsdb_script'),

    path('run_facebook_Dimitrije_Extract_TXT_IMG_script/', views.run_facebook_Dimitrije_Extract_TXT_IMG_script, name='run_facebook_Dimitrije_Extract_TXT_IMG_script'),


    # Facebook page - Ivana_K

    path('facebook_Ivana_K/', views.facebook_Ivana_K_page, name='facebook_Ivana_K_page'),
    path('run_Ivana_K_FBRSoCTonicCreatLinks_script/', views.run_Ivana_K_FBRSoCTonicCreatLinks_script, name='run_Ivana_K_FBRSoCTonicCreatLinks_script'),
    path('run_Ivana_K_tonic_FBoffers_script/', views.run_Ivana_K_tonic_FBoffers_script, name='run_Ivana_K_tonic_FBoffers_script'),
    path('run_Ivana_K_FBRSoCTonicCreatpixel_script/', views.run_Ivana_K_FBRSoCTonicCreatpixel_script, name='run_Ivana_K_FBRSoCTonicCreatpixel_script'),
    path('run_Ivana_K_FBRSoCTonicCreat_link_pixel_script/', views.run_Ivana_K_FBRSoCTonicCreat_link_pixel_script, name='run_Ivana_K_FBRSoCTonicCreat_link_pixel_script'),

    path('run_Ivana_K_predictochannels_createnew_script/', views.run_Ivana_K_predictochannels_createnew_script, name='run_Ivana_K_predictochannels_createnew_script'),
    path('run_Ivana_K_Compadochannels_createnew_script/', views.run_Ivana_K_Compadochannels_createnew_script, name='run_Ivana_K_Compadochannels_createnew_script'),
    path('run_Ivana_K_predictochannelsdb_script/', views.run_Ivana_K_predictochannelsdb_script, name='run_Ivana_K_predictochannelsdb_script'),

    path('run_facebook_Ivana_K_Extract_TXT_IMG_script/', views.run_facebook_Ivana_K_Extract_TXT_IMG_script, name='run_facebook_Ivana_K_Extract_TXT_IMG_script'),


    # Facebook page - Nemanja

    path('facebook_Nemanja/', views.facebook_Nemanja_page, name='facebook_Nemanja_page'),
    path('run_Nemanja_FBRSoCTonicCreatLinks_script/', views.run_Nemanja_FBRSoCTonicCreatLinks_script, name='run_Nemanja_FBRSoCTonicCreatLinks_script'),
    path('run_Nemanja_tonic_FBoffers_script/', views.run_Nemanja_tonic_FBoffers_script, name='run_Nemanja_tonic_FBoffers_script'),
    path('run_Nemanja_FBRSoCTonicCreatpixel_script/', views.run_Nemanja_FBRSoCTonicCreatpixel_script, name='run_Nemanja_FBRSoCTonicCreatpixel_script'),
    path('run_Nemanja_FBRSoCTonicCreat_link_pixel_script/', views.run_Nemanja_FBRSoCTonicCreat_link_pixel_script, name='run_Nemanja_FBRSoCTonicCreat_link_pixel_script'),

    path('run_Nemanja_predictochannels_createnew_script/', views.run_Nemanja_predictochannels_createnew_script, name='run_Nemanja_predictochannels_createnew_script'),
    path('run_Nemanja_Compadochannels_createnew_script/', views.run_Nemanja_Compadochannels_createnew_script, name='run_Nemanja_Compadochannels_createnew_script'),
    path('run_Nemanja_predictochannelsdb_script/', views.run_Nemanja_predictochannelsdb_script, name='run_Nemanja_predictochannelsdb_script'),

    path('run_facebook_Nemanja_Extract_TXT_IMG_script/', views.run_facebook_Nemanja_Extract_TXT_IMG_script, name='run_facebook_Nemanja_Extract_TXT_IMG_script'),



################### Facebook page







    # Mediago page - 2025


    path('run_rsoccreatetonicoffersmediago_script/', views.run_rsoccreatetonicoffersmediago_script, name='run_rsoccreatetonicoffersmediago_script'),
    path('run_tonic_mediagooffers_script/', views.run_tonic_mediagooffers_script, name='run_tonic_mediagooffers_script'),



    # Mediago page - Bulk


    path('mediago_Bulk/', views.mediago_Bulk_page, name='mediago_Bulk_page'),
    path('run_Bulk_rsoccreatetonicoffersmediago_script/', views.run_Bulk_rsoccreatetonicoffersmediago_script, name='run_Bulk_rsoccreatetonicoffersmediago_script'),
    path('run_Bulk_tonic_mediagooffers_script/', views.run_Bulk_tonic_mediagooffers_script, name='run_Bulk_tonic_mediagooffers_script'),

    path('run_bulk_MediaGoShortneHeadlines_script/', views.run_bulk_MediaGoShortneHeadlines_script, name='run_bulk_MediaGoShortneHeadlines_script'),

    path('run_MediaGo_bulk__tchannels_createnew_script/', views.run_MediaGo_bulk__tchannels_createnew_script, name='run_MediaGo_bulk__tchannels_createnew_script'),
    path('run_MediaGo_bulk__tchannelsdb_script/', views.run_MediaGo_bulk__tchannelsdb_script, name='run_MediaGo_bulk__tchannelsdb_script'),

    path('run_MediaGo_Upload_PAW_script/', views.run_MediaGo_Upload_PAW_script, name='run_MediaGo_Upload_PAW_script'),


    # Mediago page - Or


    path('mediago_Or/', views.mediago_Or_page, name='mediago_Or_page'),
    path('run_Or_rsoccreatetonicoffersmediago_script/', views.run_Or_rsoccreatetonicoffersmediago_script, name='run_Or_rsoccreatetonicoffersmediago_script'),
    path('run_Or_tonic_mediagooffers_script/', views.run_Or_tonic_mediagooffers_script, name='run_Or_tonic_mediagooffers_script'),

    path('run_MediaGo_Or__tchannels_createnew_script/', views.run_MediaGo_Or__tchannels_createnew_script, name='run_MediaGo_Or__tchannels_createnew_script'),
    path('run_MediaGo_Or__tchannelsdb_script/', views.run_MediaGo_Or__tchannelsdb_script, name='run_MediaGo_Or__tchannelsdb_script'),


    # Mediago page - Yoav


    path('mediago_Yoav/', views.mediago_Yoav_page, name='mediago_Yoav_page'),
    path('run_Yoav_rsoccreatetonicoffersmediago_script/', views.run_Yoav_rsoccreatetonicoffersmediago_script, name='run_Yoav_rsoccreatetonicoffersmediago_script'),
    path('run_Yoav_tonic_mediagooffers_script/', views.run_Yoav_tonic_mediagooffers_script, name='run_Yoav_tonic_mediagooffers_script'),

    path('run_MediaGo_Yoav__tchannels_createnew_script/', views.run_MediaGo_Yoav__tchannels_createnew_script, name='run_MediaGo_Yoav__tchannels_createnew_script'),
    path('run_MediaGo_Yoav__tchannelsdb_script/', views.run_MediaGo_Yoav__tchannelsdb_script, name='run_MediaGo_Yoav__tchannelsdb_script'),


    # Mediago page - Omer


    path('mediago_Omer/', views.mediago_Omer_page, name='mediago_Omer_page'),
    path('run_Omer_rsoccreatetonicoffersmediago_script/', views.run_Omer_rsoccreatetonicoffersmediago_script, name='run_Omer_rsoccreatetonicoffersmediago_script'),
    path('run_Omer_tonic_mediagooffers_script/', views.run_Omer_tonic_mediagooffers_script, name='run_Omer_tonic_mediagooffers_script'),

    path('run_MediaGo_Omer__tchannels_createnew_script/', views.run_MediaGo_Omer__tchannels_createnew_script, name='run_MediaGo_Omer__tchannels_createnew_script'),
    path('run_MediaGo_Omer__tchannelsdb_script/', views.run_MediaGo_Omer__tchannelsdb_script, name='run_MediaGo_Omer__tchannelsdb_script'),


    # Mediago page - Maya


    path('mediago_Maya/', views.mediago_Maya_page, name='mediago_Maya_page'),
    path('run_Maya_rsoccreatetonicoffersmediago_script/', views.run_Maya_rsoccreatetonicoffersmediago_script, name='run_Maya_rsoccreatetonicoffersmediago_script'),
    path('run_Maya_tonic_mediagooffers_script/', views.run_Maya_tonic_mediagooffers_script, name='run_Maya_tonic_mediagooffers_script'),

    path('run_MediaGo_Maya__tchannels_createnew_script/', views.run_MediaGo_Maya__tchannels_createnew_script, name='run_MediaGo_Maya__tchannels_createnew_script'),
    path('run_MediaGo_Maya__tchannelsdb_script/', views.run_MediaGo_Maya__tchannelsdb_script, name='run_MediaGo_Maya__tchannelsdb_script'),



################### Tiktok page





    # Tiktok page - Bulk


    path('tiktok_Bulk/', views.tiktok_Bulk_page, name='tiktok_Bulk_page'),
    path('run_Bulk_TKRSoCTonicCreat_link_pixel_script/', views.run_Bulk_TKRSoCTonicCreat_link_pixel_script, name='run_Bulk_TKRSoCTonicCreat_link_pixel_script'),
    path('run_Bulk_tonic_TKoffers_script/', views.run_Bulk_tonic_TKoffers_script, name='run_Bulk_tonic_TKoffers_script'),
    path('run_Bulk_TKRSoCTonicCreatLinks_script/', views.run_Bulk_TKRSoCTonicCreatLinks_script, name='run_Bulk_TKRSoCTonicCreatLinks_script'),
    path('run_Bulk_TKRSoCTonicCreatpixel_script/', views.run_Bulk_TKRSoCTonicCreatpixel_script, name='run_Bulk_TKRSoCTonicCreatpixel_script'),


    path('run_Tiktok_bulk__tchannels_createnew_script/', views.run_Tiktok_bulk__tchannels_createnew_script, name='run_Tiktok_bulk__tchannels_createnew_script'),
    path('run_Tiktok_bulk__tchannelsdb_script/', views.run_Tiktok_bulk__tchannelsdb_script, name='run_Tiktok_bulk__tchannelsdb_script'),


    path('run_Bulk_TKRSoCTonicCreat_link_pixel_Dup_script/', views.run_Bulk_TKRSoCTonicCreat_link_pixel_Dup_script, name='run_Bulk_TKRSoCTonicCreat_link_pixel_Dup_script'),
    path('run_Bulk_TKRSoCTonicCreatpixel_Dup_script/', views.run_Bulk_TKRSoCTonicCreatpixel_Dup_script, name='run_Bulk_TKRSoCTonicCreatpixel_Dup_script'),


    path('run_Tiktok_Bulk_Manual_imagescut_script/', views.run_Tiktok_Bulk_Manual_imagescut_script, name='run_Tiktok_Bulk_Manual_imagescut_script'),
    path('run_TikTokCreateScript_script/', views.run_TikTokCreateScript_script, name='run_TikTokCreateScript_script'),


    path('run_Bulk_tiktok_ads_uploader_v5_script/', views.run_Bulk_tiktok_ads_uploader_v5_script, name='run_Bulk_tiktok_ads_uploader_v5_script'),
    path('run_Bulk_tiktok_duplicator_2026_script/', views.run_Bulk_tiktok_duplicator_2026_script, name='run_Bulk_tiktok_duplicator_2026_script'),


    # Tiktok page - Omer


    path('tiktok_Omer/', views.tiktok_Omer_page, name='tiktok_Omer_page'),
    path('run_Omer_TKRSoCTonicCreat_link_pixel_script/', views.run_Omer_TKRSoCTonicCreat_link_pixel_script, name='run_Omer_TKRSoCTonicCreat_link_pixel_script'),
    path('run_Omer_tonic_TKoffers_script/', views.run_Omer_tonic_TKoffers_script, name='run_Omer_tonic_TKoffers_script'),
    path('run_Omer_TKRSoCTonicCreatLinks_script/', views.run_Omer_TKRSoCTonicCreatLinks_script, name='run_Omer_TKRSoCTonicCreatLinks_script'),
    path('run_Omer_TKRSoCTonicCreatpixel_script/', views.run_Omer_TKRSoCTonicCreatpixel_script, name='run_Omer_TKRSoCTonicCreatpixel_script'),


    path('run_Tiktok_Omer__tchannels_createnew_script/', views.run_Tiktok_Omer__tchannels_createnew_script, name='run_Tiktok_Omer__tchannels_createnew_script'),
    path('run_Tiktok_Omer__tchannelsdb_script/', views.run_Tiktok_Omer__tchannelsdb_script, name='run_Tiktok_Omer__tchannelsdb_script'),



    # Tiktok page - Maya


    path('tiktok_Maya/', views.tiktok_Maya_page, name='tiktok_Maya_page'),
    path('run_Maya_TKRSoCTonicCreat_link_pixel_script/', views.run_Maya_TKRSoCTonicCreat_link_pixel_script, name='run_Maya_TKRSoCTonicCreat_link_pixel_script'),
    path('run_Maya_tonic_TKoffers_script/', views.run_Maya_tonic_TKoffers_script, name='run_Maya_tonic_TKoffers_script'),
    path('run_Maya_TKRSoCTonicCreatLinks_script/', views.run_Maya_TKRSoCTonicCreatLinks_script, name='run_Maya_TKRSoCTonicCreatLinks_script'),
    path('run_Maya_TKRSoCTonicCreatpixel_script/', views.run_Maya_TKRSoCTonicCreatpixel_script, name='run_Maya_TKRSoCTonicCreatpixel_script'),


    path('run_Tiktok_Maya__tchannels_createnew_script/', views.run_Tiktok_Maya__tchannels_createnew_script, name='run_Tiktok_Maya__tchannels_createnew_script'),
    path('run_Tiktok_Maya__tchannelsdb_script/', views.run_Tiktok_Maya__tchannelsdb_script, name='run_Tiktok_Maya__tchannelsdb_script'),



    # Tiktok page - Matan


    path('tiktok_Matan/', views.tiktok_Matan_page, name='tiktok_Matan_page'),
    path('run_Matan_TKRSoCTonicCreat_link_pixel_script/', views.run_Matan_TKRSoCTonicCreat_link_pixel_script, name='run_Matan_TKRSoCTonicCreat_link_pixel_script'),
    path('run_Matan_tonic_TKoffers_script/', views.run_Matan_tonic_TKoffers_script, name='run_Matan_tonic_TKoffers_script'),
    path('run_Matan_TKRSoCTonicCreatLinks_script/', views.run_Matan_TKRSoCTonicCreatLinks_script, name='run_Matan_TKRSoCTonicCreatLinks_script'),
    path('run_Matan_TKRSoCTonicCreatpixel_script/', views.run_Matan_TKRSoCTonicCreatpixel_script, name='run_Matan_TKRSoCTonicCreatpixel_script'),


    path('run_Tiktok_Matan__tchannels_createnew_script/', views.run_Tiktok_Matan__tchannels_createnew_script, name='run_Tiktok_Matan__tchannels_createnew_script'),
    path('run_Tiktok_Matan__tchannelsdb_script/', views.run_Tiktok_Matan__tchannelsdb_script, name='run_Tiktok_Matan__tchannelsdb_script'),



    # Tiktok page - Elran


    path('tiktok_Elran/', views.tiktok_Elran_page, name='tiktok_Elran_page'),
    path('run_Elran_TKRSoCTonicCreat_link_pixel_script/', views.run_Elran_TKRSoCTonicCreat_link_pixel_script, name='run_Elran_TKRSoCTonicCreat_link_pixel_script'),
    path('run_Elran_tonic_TKoffers_script/', views.run_Elran_tonic_TKoffers_script, name='run_Elran_tonic_TKoffers_script'),
    path('run_Elran_TKRSoCTonicCreatLinks_script/', views.run_Elran_TKRSoCTonicCreatLinks_script, name='run_Elran_TKRSoCTonicCreatLinks_script'),
    path('run_Elran_TKRSoCTonicCreatpixel_script/', views.run_Elran_TKRSoCTonicCreatpixel_script, name='run_Elran_TKRSoCTonicCreatpixel_script'),


    path('run_Tiktok_Elran__tchannels_createnew_script/', views.run_Tiktok_Elran__tchannels_createnew_script, name='run_Tiktok_Elran__tchannels_createnew_script'),
    path('run_Tiktok_Elran__tchannelsdb_script/', views.run_Tiktok_Elran__tchannelsdb_script, name='run_Tiktok_Elran__tchannelsdb_script'),



################### WTHMM page



    # Slavo


    path('run_Slavo_keywordsanalyze_script/', views.run_Slavo_keywordsanalyze_script, name='run_Slavo_keywordsanalyze_script'),
    path('run_Slavo_keywordstokeywords_v3_script/', views.run_Slavo_keywordstokeywords_v3_script, name='run_Slavo_keywordstokeywords_v3_script'),


    # Dimitrije


    path('run_Dimitrije_keywordsanalyze_script/', views.run_Dimitrije_keywordsanalyze_script, name='run_Dimitrije_keywordsanalyze_script'),
    path('run_Dimitrije_keywordstokeywords_v3_script/', views.run_Dimitrije_keywordstokeywords_v3_script, name='run_Dimitrije_keywordstokeywords_v3_script'),


    # Ivana_K


    path('run_Ivana_K_keywordsanalyze_script/', views.run_Ivana_K_keywordsanalyze_script, name='run_Ivana_K_keywordsanalyze_script'),
    path('run_Ivana_K_keywordstokeywords_v3_script/', views.run_Ivana_K_keywordstokeywords_v3_script, name='run_Ivana_K_keywordstokeywords_v3_script'),


    # Jelena


    path('run_Jelena_keywordsanalyze_script/', views.run_Jelena_keywordsanalyze_script, name='run_Jelena_keywordsanalyze_script'),
    path('run_Jelena_keywordstokeywords_v3_script/', views.run_Jelena_keywordstokeywords_v3_script, name='run_Jelena_keywordstokeywords_v3_script'),


    # Nemanja


    path('run_Nemanja_keywordsanalyze_script/', views.run_Nemanja_keywordsanalyze_script, name='run_Nemanja_keywordsanalyze_script'),
    path('run_Nemanja_keywordstokeywords_v3_script/', views.run_Nemanja_keywordstokeywords_v3_script, name='run_Nemanja_keywordstokeywords_v3_script'),


    # Elad


    path('run_Elad_keywordsanalyze_script/', views.run_Elad_keywordsanalyze_script, name='run_Elad_keywordsanalyze_script'),
    path('run_Elad_keywordstokeywords_v3_script/', views.run_Elad_keywordstokeywords_v3_script, name='run_Elad_keywordstokeywords_v3_script'),

    path('run_Elad_creatives_builder_script/', views.run_Elad_creatives_builder_script, name='run_Elad_creatives_builder_script'),


    # Elran


    path('run_Elran_keywordsanalyze_script/', views.run_Elran_keywordsanalyze_script, name='run_Elran_keywordsanalyze_script'),
    path('run_Elran_keywordstokeywords_v3_script/', views.run_Elran_keywordstokeywords_v3_script, name='run_Elran_keywordstokeywords_v3_script'),

    path('run_Elran_creatives_builder_script/', views.run_Elran_creatives_builder_script, name='run_Elran_creatives_builder_script'),


    # Omer


    path('run_Omer_keywordsanalyze_script/', views.run_Omer_keywordsanalyze_script, name='run_Omer_keywordsanalyze_script'),
    path('run_Omer_keywordstokeywords_v3_script/', views.run_Omer_keywordstokeywords_v3_script, name='run_Omer_keywordstokeywords_v3_script'),

    path('run_Omer_creatives_builder_script/', views.run_Omer_creatives_builder_script, name='run_Omer_creatives_builder_script'),


    # Dina


    path('run_Dina_keywordsanalyze_script/', views.run_Dina_keywordsanalyze_script, name='run_Dina_keywordsanalyze_script'),
    path('run_Dina_keywordstokeywords_v3_script/', views.run_Dina_keywordstokeywords_v3_script, name='run_Dina_keywordstokeywords_v3_script'),

    path('run_Dina_creatives_builder_script/', views.run_Dina_creatives_builder_script, name='run_Dina_creatives_builder_script'),


    # Yoav


    path('run_Yoav_keywordsanalyze_script/', views.run_Yoav_keywordsanalyze_script, name='run_Yoav_keywordsanalyze_script'),
    path('run_Yoav_keywordstokeywords_v3_script/', views.run_Yoav_keywordstokeywords_v3_script, name='run_Yoav_keywordstokeywords_v3_script'),

    path('run_Yoav_creatives_builder_script/', views.run_Yoav_creatives_builder_script, name='run_Yoav_creatives_builder_script'),


    # Matan


    path('run_Matan_keywordsanalyze_script/', views.run_Matan_keywordsanalyze_script, name='run_Matan_keywordsanalyze_script'),
    path('run_Matan_keywordstokeywords_v3_script/', views.run_Matan_keywordstokeywords_v3_script, name='run_Matan_keywordstokeywords_v3_script'),



    # Or


    path('run_Or_keywordsanalyze_script/', views.run_Or_keywordsanalyze_script, name='run_Or_keywordsanalyze_script'),
    path('run_Or_keywordstokeywords_v3_script/', views.run_Or_keywordstokeywords_v3_script, name='run_Or_keywordstokeywords_v3_script'),

    path('run_Or_creatives_builder_script/', views.run_Or_creatives_builder_script, name='run_Or_creatives_builder_script'),






    # Maya


    path('run_Maya_keywordsanalyze_script/', views.run_Maya_keywordsanalyze_script, name='run_Maya_keywordsanalyze_script'),
    path('run_Maya_keywordstokeywords_v3_script/', views.run_Maya_keywordstokeywords_v3_script, name='run_Maya_keywordstokeywords_v3_script'),

    path('run_Maya_creatives_builder_script/', views.run_Maya_creatives_builder_script, name='run_Maya_creatives_builder_script'),







############ RSS page




    path('run_fetch_all_articles_summaries_script/', views.run_fetch_all_articles_summaries_script, name='run_fetch_all_articles_summaries_script'),
    path('run_fetch_specific_articles_with_content_script/', views.run_fetch_specific_articles_with_content_script, name='run_fetch_specific_articles_with_content_script'),
    path('run_articles_db_manager_script/', views.run_articles_db_manager_script, name='run_articles_db_manager_script'),
    path('run_getdataofarticleforrss_script/', views.run_getdataofarticleforrss_script, name='run_getdataofarticleforrss_script'),
    path('run_rss_writer_script/', views.run_rss_writer_script, name='run_rss_writer_script'),



############ Sasha Test



    path('run_Sasha_creatives_builder_script/', views.run_Sasha_creatives_builder_script, name='run_Sasha_creatives_builder_script'),




########################################################################


    #### Elad #####


    path('media_buyer_Elad_page/', views.media_buyer_Elad_page, name='media_buyer_Elad_page'),

    path('run_Elad_FBRSoCTonicCreatLinks_script/', views.run_Elad_FBRSoCTonicCreatLinks_script, name='run_Elad_FBRSoCTonicCreatLinks_script'),
    path('run_Elad_tonic_FBoffers_script/', views.run_Elad_tonic_FBoffers_script, name='run_Elad_tonic_FBoffers_script'),
    path('run_Elad_FBRSoCTonicCreatpixel_script/', views.run_Elad_FBRSoCTonicCreatpixel_script, name='run_Elad_FBRSoCTonicCreatpixel_script'),
    path('run_Elad_FBRSoCTonicCreat_link_pixel_script/', views.run_Elad_FBRSoCTonicCreat_link_pixel_script, name='run_Elad_FBRSoCTonicCreat_link_pixel_script'),

    path('run_facebook_Elad_tc_channels_createnew_script/', views.run_facebook_Elad_tc_channels_createnew_script, name='run_facebook_Elad_tc_channels_createnew_script'),
    path('run_facebook_Elad_tc_channelsdb_script/', views.run_facebook_Elad_tc_channelsdb_script, name='run_facebook_Elad_tc_channelsdb_script'),
    path('run_facebook_Elad_Extract_TXT_IMG_script/', views.run_facebook_Elad_Extract_TXT_IMG_script, name='run_facebook_Elad_Extract_TXT_IMG_script'),

    path('run_Elad_fb_uploader_v26_script/', views.run_Elad_fb_uploader_v26_script, name='run_Elad_fb_uploader_v26_script'),


    path('run_Elad_rsoctoniccreateofferesoutbrain_script/', views.run_Elad_rsoctoniccreateofferesoutbrain_script, name='run_Elad_rsoctoniccreateofferesoutbrain_script'),
    path('run_Elad_tonic_outbrainoffers_script/', views.run_Elad_tonic_outbrainoffers_script, name='run_Elad_tonic_outbrainoffers_script'),

    path('run_outbrain_Elad__tchannels_createnew_script/', views.run_outbrain_Elad__tchannels_createnew_script, name='run_outbrain_Elad__tchannels_createnew_script'),
    path('run_outbrain_Elad__tchannelsdb_script/', views.run_outbrain_Elad__tchannelsdb_script, name='run_outbrain_Elad__tchannelsdb_script'),

    path('run_Elad_outbrain_uploader_script/', views.run_Elad_outbrain_uploader_script, name='run_Elad_outbrain_uploader_script'),





    #### Or #####


    path('media_buyer_Or_page/', views.media_buyer_Or_page, name='media_buyer_Or_page'),

    path('run_Or_FBRSoCTonicCreatLinks_script/', views.run_Or_FBRSoCTonicCreatLinks_script, name='run_Or_FBRSoCTonicCreatLinks_script'),
    path('run_Or_tonic_FBoffers_script/', views.run_Or_tonic_FBoffers_script, name='run_Or_tonic_FBoffers_script'),
    path('run_Or_FBRSoCTonicCreatpixel_script/', views.run_Or_FBRSoCTonicCreatpixel_script, name='run_Or_FBRSoCTonicCreatpixel_script'),
    path('run_Or_FBRSoCTonicCreat_link_pixel_script/', views.run_Or_FBRSoCTonicCreat_link_pixel_script, name='run_Or_FBRSoCTonicCreat_link_pixel_script'),

    path('run_facebook_Or_tc_channels_createnew_script/', views.run_facebook_Or_tc_channels_createnew_script, name='run_facebook_Or_tc_channels_createnew_script'),
    path('run_facebook_Or_tc_channelsdb_script/', views.run_facebook_Or_tc_channelsdb_script, name='run_facebook_Or_tc_channelsdb_script'),
    path('run_facebook_Or_Extract_TXT_IMG_script/', views.run_facebook_Or_Extract_TXT_IMG_script, name='run_facebook_Or_Extract_TXT_IMG_script'),

    path('run_Or_fb_uploader_v26_script/', views.run_Or_fb_uploader_v26_script, name='run_Or_fb_uploader_v26_script'),


    path('run_Or_rsoctoniccreateofferesoutbrain_script/', views.run_Or_rsoctoniccreateofferesoutbrain_script, name='run_Or_rsoctoniccreateofferesoutbrain_script'),
    path('run_Or_tonic_outbrainoffers_script/', views.run_Or_tonic_outbrainoffers_script, name='run_Or_tonic_outbrainoffers_script'),

    path('run_outbrain_Or__tchannels_createnew_script/', views.run_outbrain_Or__tchannels_createnew_script, name='run_outbrain_Or__tchannels_createnew_script'),
    path('run_outbrain_Or__tchannelsdb_script/', views.run_outbrain_Or__tchannelsdb_script, name='run_outbrain_Or__tchannelsdb_script'),

    path('run_Or_outbrain_uploader_script/', views.run_Or_outbrain_uploader_script, name='run_Or_outbrain_uploader_script'),





    #### Yoav #####


    path('media_buyer_Yoav_page/', views.media_buyer_Yoav_page, name='media_buyer_Yoav_page'),

    path('run_Yoav_FBRSoCTonicCreatLinks_script/', views.run_Yoav_FBRSoCTonicCreatLinks_script, name='run_Yoav_FBRSoCTonicCreatLinks_script'),
    path('run_Yoav_tonic_FBoffers_script/', views.run_Yoav_tonic_FBoffers_script, name='run_Yoav_tonic_FBoffers_script'),
    path('run_Yoav_FBRSoCTonicCreatpixel_script/', views.run_Yoav_FBRSoCTonicCreatpixel_script, name='run_Yoav_FBRSoCTonicCreatpixel_script'),
    path('run_Yoav_FBRSoCTonicCreat_link_pixel_script/', views.run_Yoav_FBRSoCTonicCreat_link_pixel_script, name='run_Yoav_FBRSoCTonicCreat_link_pixel_script'),

    path('run_facebook_Yoav_tc_channels_createnew_script/', views.run_facebook_Yoav_tc_channels_createnew_script, name='run_facebook_Yoav_tc_channels_createnew_script'),
    path('run_facebook_Yoav_tc_channelsdb_script/', views.run_facebook_Yoav_tc_channelsdb_script, name='run_facebook_Yoav_tc_channelsdb_script'),
    path('run_facebook_Yoav_Extract_TXT_IMG_script/', views.run_facebook_Yoav_Extract_TXT_IMG_script, name='run_facebook_Yoav_Extract_TXT_IMG_script'),

    path('run_Yoav_fb_uploader_v26_script/', views.run_Yoav_fb_uploader_v26_script, name='run_Yoav_fb_uploader_v26_script'),


    path('run_Yoav_rsoctoniccreateofferesoutbrain_script/', views.run_Yoav_rsoctoniccreateofferesoutbrain_script, name='run_Yoav_rsoctoniccreateofferesoutbrain_script'),
    path('run_Yoav_tonic_outbrainoffers_script/', views.run_Yoav_tonic_outbrainoffers_script, name='run_Yoav_tonic_outbrainoffers_script'),

    path('run_outbrain_Yoav__tchannels_createnew_script/', views.run_outbrain_Yoav__tchannels_createnew_script, name='run_outbrain_Yoav__tchannels_createnew_script'),
    path('run_outbrain_Yoav__tchannelsdb_script/', views.run_outbrain_Yoav__tchannelsdb_script, name='run_outbrain_Yoav__tchannelsdb_script'),

    path('run_Yoav_outbrain_uploader_script/', views.run_Yoav_outbrain_uploader_script, name='run_Yoav_outbrain_uploader_script'),







    #### Dina #####


    path('media_buyer_Dina_page/', views.media_buyer_Dina_page, name='media_buyer_Dina_page'),

    path('run_Dina_FBRSoCTonicCreatLinks_script/', views.run_Dina_FBRSoCTonicCreatLinks_script, name='run_Dina_FBRSoCTonicCreatLinks_script'),
    path('run_Dina_tonic_FBoffers_script/', views.run_Dina_tonic_FBoffers_script, name='run_Dina_tonic_FBoffers_script'),
    path('run_Dina_FBRSoCTonicCreatpixel_script/', views.run_Dina_FBRSoCTonicCreatpixel_script, name='run_Dina_FBRSoCTonicCreatpixel_script'),
    path('run_Dina_FBRSoCTonicCreat_link_pixel_script/', views.run_Dina_FBRSoCTonicCreat_link_pixel_script, name='run_Dina_FBRSoCTonicCreat_link_pixel_script'),

    path('run_facebook_Dina_tc_channels_createnew_script/', views.run_facebook_Dina_tc_channels_createnew_script, name='run_facebook_Dina_tc_channels_createnew_script'),
    path('run_facebook_Dina_tc_channelsdb_script/', views.run_facebook_Dina_tc_channelsdb_script, name='run_facebook_Dina_tc_channelsdb_script'),
    path('run_facebook_Dina_Extract_TXT_IMG_script/', views.run_facebook_Dina_Extract_TXT_IMG_script, name='run_facebook_Dina_Extract_TXT_IMG_script'),

    path('run_Dina_fb_uploader_v26_script/', views.run_Dina_fb_uploader_v26_script, name='run_Dina_fb_uploader_v26_script'),


    path('run_Dina_rsoctoniccreateofferesoutbrain_script/', views.run_Dina_rsoctoniccreateofferesoutbrain_script, name='run_Dina_rsoctoniccreateofferesoutbrain_script'),
    path('run_Dina_tonic_outbrainoffers_script/', views.run_Dina_tonic_outbrainoffers_script, name='run_Dina_tonic_outbrainoffers_script'),

    path('run_outbrain_Dina__tchannels_createnew_script/', views.run_outbrain_Dina__tchannels_createnew_script, name='run_outbrain_Dina__tchannels_createnew_script'),
    path('run_outbrain_Dina__tchannelsdb_script/', views.run_outbrain_Dina__tchannelsdb_script, name='run_outbrain_Dina__tchannelsdb_script'),

    path('run_Dina_outbrain_uploader_script/', views.run_Dina_outbrain_uploader_script, name='run_Dina_outbrain_uploader_script'),









    #### Elran #####


    path('media_buyer_Elran_page/', views.media_buyer_Elran_page, name='media_buyer_Elran_page'),

    path('run_Elran_FBRSoCTonicCreatLinks_script/', views.run_Elran_FBRSoCTonicCreatLinks_script, name='run_Elran_FBRSoCTonicCreatLinks_script'),
    path('run_Elran_tonic_FBoffers_script/', views.run_Elran_tonic_FBoffers_script, name='run_Elran_tonic_FBoffers_script'),
    path('run_Elran_FBRSoCTonicCreatpixel_script/', views.run_Elran_FBRSoCTonicCreatpixel_script, name='run_Elran_FBRSoCTonicCreatpixel_script'),
    path('run_Elran_FBRSoCTonicCreat_link_pixel_script/', views.run_Elran_FBRSoCTonicCreat_link_pixel_script, name='run_Elran_FBRSoCTonicCreat_link_pixel_script'),

    path('run_facebook_Elran_tc_channels_createnew_script/', views.run_facebook_Elran_tc_channels_createnew_script, name='run_facebook_Elran_tc_channels_createnew_script'),
    path('run_facebook_Elran_tc_channelsdb_script/', views.run_facebook_Elran_tc_channelsdb_script, name='run_facebook_Elran_tc_channelsdb_script'),
    path('run_facebook_Elran_Extract_TXT_IMG_script/', views.run_facebook_Elran_Extract_TXT_IMG_script, name='run_facebook_Elran_Extract_TXT_IMG_script'),

    path('run_Elran_fb_uploader_v26_script/', views.run_Elran_fb_uploader_v26_script, name='run_Elran_fb_uploader_v26_script'),


    path('run_Elran_rsoctoniccreateofferesoutbrain_script/', views.run_Elran_rsoctoniccreateofferesoutbrain_script, name='run_Elran_rsoctoniccreateofferesoutbrain_script'),
    path('run_Elran_tonic_outbrainoffers_script/', views.run_Elran_tonic_outbrainoffers_script, name='run_Elran_tonic_outbrainoffers_script'),

    path('run_outbrain_Elran__tchannels_createnew_script/', views.run_outbrain_Elran__tchannels_createnew_script, name='run_outbrain_Elran__tchannels_createnew_script'),
    path('run_outbrain_Elran__tchannelsdb_script/', views.run_outbrain_Elran__tchannelsdb_script, name='run_outbrain_Elran__tchannelsdb_script'),

    path('run_Elran_outbrain_uploader_script/', views.run_Elran_outbrain_uploader_script, name='run_Elran_outbrain_uploader_script'),












    #### Guy #####


    path('media_buyer_Guy_page/', views.media_buyer_Guy_page, name='media_buyer_Guy_page'),

    path('run_Guy_FBRSoCTonicCreatLinks_script/', views.run_Guy_FBRSoCTonicCreatLinks_script, name='run_Guy_FBRSoCTonicCreatLinks_script'),
    path('run_Guy_tonic_FBoffers_script/', views.run_Guy_tonic_FBoffers_script, name='run_Guy_tonic_FBoffers_script'),
    path('run_Guy_FBRSoCTonicCreatpixel_script/', views.run_Guy_FBRSoCTonicCreatpixel_script, name='run_Guy_FBRSoCTonicCreatpixel_script'),
    path('run_Guy_FBRSoCTonicCreat_link_pixel_script/', views.run_Guy_FBRSoCTonicCreat_link_pixel_script, name='run_Guy_FBRSoCTonicCreat_link_pixel_script'),

    path('run_facebook_Guy_tc_channels_createnew_script/', views.run_facebook_Guy_tc_channels_createnew_script, name='run_facebook_Guy_tc_channels_createnew_script'),
    path('run_facebook_Guy_tc_channelsdb_script/', views.run_facebook_Guy_tc_channelsdb_script, name='run_facebook_Guy_tc_channelsdb_script'),
    path('run_facebook_Guy_Extract_TXT_IMG_script/', views.run_facebook_Guy_Extract_TXT_IMG_script, name='run_facebook_Guy_Extract_TXT_IMG_script'),

    path('run_Guy_fb_uploader_v26_script/', views.run_Guy_fb_uploader_v26_script, name='run_Guy_fb_uploader_v26_script'),


    path('run_Guy_rsoctoniccreateofferesoutbrain_script/', views.run_Guy_rsoctoniccreateofferesoutbrain_script, name='run_Guy_rsoctoniccreateofferesoutbrain_script'),
    path('run_Guy_tonic_outbrainoffers_script/', views.run_Guy_tonic_outbrainoffers_script, name='run_Guy_tonic_outbrainoffers_script'),

    path('run_outbrain_Guy__tchannels_createnew_script/', views.run_outbrain_Guy__tchannels_createnew_script, name='run_outbrain_Guy__tchannels_createnew_script'),
    path('run_outbrain_Guy__tchannelsdb_script/', views.run_outbrain_Guy__tchannelsdb_script, name='run_outbrain_Guy__tchannelsdb_script'),

    path('run_Guy_outbrain_uploader_script/', views.run_Guy_outbrain_uploader_script, name='run_Guy_outbrain_uploader_script'),



    path('run_Guy_tonic_taboolaoffers_script/', views.run_Guy_tonic_taboolaoffers_script, name='run_Guy_tonic_taboolaoffers_script'),
    path('run_Guy_rsoctoniccreateofferestaboola_script/', views.run_Guy_rsoctoniccreateofferestaboola_script, name='run_Guy_rsoctoniccreateofferestaboola_script'),

    path('run_Guy_tabduplicatorfortest_s1_script/', views.run_Guy_tabduplicatorfortest_s1_script, name='run_Guy_tabduplicatorfortest_s1_script'),
    path('run_Guy_tabduplicatorfortest_Inuvo_script/', views.run_Guy_tabduplicatorfortest_Inuvo_script, name='run_Guy_tabduplicatorfortest_Inuvo_script'),
    path('run_Guy_tabduplicatorfortest_AFD_script/', views.run_Guy_tabduplicatorfortest_AFD_script, name='run_Guy_tabduplicatorfortest_AFD_script'),
    path('run_Guy_tabduplicatorfortest_RSOC_script/', views.run_Guy_tabduplicatorfortest_RSOC_script, name='run_Guy_tabduplicatorfortest_RSOC_script'),
    path('run_Guy_tabduplicatorfortest_TC_script/', views.run_Guy_tabduplicatorfortest_TC_script, name='run_Guy_tabduplicatorfortest_TC_script'),

    path('run_taboola_Guy_newpolicycheckforall_script/', views.run_taboola_Guy_newpolicycheckforall_script, name='run_taboola_Guy_newpolicycheckforall_script'),


    path('run_taboola_Guy__tchannels_createnew_script/', views.run_taboola_Guy__tchannels_createnew_script, name='run_taboola_Guy__tchannels_createnew_script'),
    path('run_taboola_Guy__tchannelsdb_script/', views.run_taboola_Guy__tchannelsdb_script, name='run_taboola_Guy__tchannelsdb_script'),

    path('run_Guy_upload_taboola_creatives_S1_script/', views.run_Guy_upload_taboola_creatives_S1_script, name='run_Guy_upload_taboola_creatives_S1_script'),
    path('run_Guy_upload_taboola_creatives_TC_script/', views.run_Guy_upload_taboola_creatives_TC_script, name='run_Guy_upload_taboola_creatives_TC_script'),
    path('run_Guy_upload_taboola_creatives_RSOC_script/', views.run_Guy_upload_taboola_creatives_RSOC_script, name='run_Guy_upload_taboola_creatives_RSOC_script'),
    path('run_Guy_upload_taboola_creatives_Inuvo_script/', views.run_Guy_upload_taboola_creatives_Inuvo_script, name='run_Guy_upload_taboola_creatives_Inuvo_script'),

    path('run_Guy_keywordsanalyze_script/', views.run_Guy_keywordsanalyze_script, name='run_Guy_keywordsanalyze_script'),
    path('run_Guy_keywordstokeywords_v3_script/', views.run_Guy_keywordstokeywords_v3_script, name='run_Guy_keywordstokeywords_v3_script'),
    path('run_Guy_creatives_builder_script/', views.run_Guy_creatives_builder_script, name='run_Guy_creatives_builder_script'),




    #### Sahar #####




    path('media_buyer_Sahar_page/', views.media_buyer_Sahar_page, name='media_buyer_Sahar_page'),

    path('run_Sahar_FBRSoCTonicCreatLinks_script/', views.run_Sahar_FBRSoCTonicCreatLinks_script, name='run_Sahar_FBRSoCTonicCreatLinks_script'),
    path('run_Sahar_tonic_FBoffers_script/', views.run_Sahar_tonic_FBoffers_script, name='run_Sahar_tonic_FBoffers_script'),
    path('run_Sahar_FBRSoCTonicCreatpixel_script/', views.run_Sahar_FBRSoCTonicCreatpixel_script, name='run_Sahar_FBRSoCTonicCreatpixel_script'),
    path('run_Sahar_FBRSoCTonicCreat_link_pixel_script/', views.run_Sahar_FBRSoCTonicCreat_link_pixel_script, name='run_Sahar_FBRSoCTonicCreat_link_pixel_script'),

    path('run_facebook_Sahar_tc_channels_createnew_script/', views.run_facebook_Sahar_tc_channels_createnew_script, name='run_facebook_Sahar_tc_channels_createnew_script'),
    path('run_facebook_Sahar_tc_channelsdb_script/', views.run_facebook_Sahar_tc_channelsdb_script, name='run_facebook_Sahar_tc_channelsdb_script'),
    path('run_facebook_Sahar_Extract_TXT_IMG_script/', views.run_facebook_Sahar_Extract_TXT_IMG_script, name='run_facebook_Sahar_Extract_TXT_IMG_script'),

    path('run_Sahar_fb_uploader_v26_script/', views.run_Sahar_fb_uploader_v26_script, name='run_Sahar_fb_uploader_v26_script'),


    path('run_Sahar_rsoctoniccreateofferesoutbrain_script/', views.run_Sahar_rsoctoniccreateofferesoutbrain_script, name='run_Sahar_rsoctoniccreateofferesoutbrain_script'),
    path('run_Sahar_tonic_outbrainoffers_script/', views.run_Sahar_tonic_outbrainoffers_script, name='run_Sahar_tonic_outbrainoffers_script'),

    path('run_outbrain_Sahar__tchannels_createnew_script/', views.run_outbrain_Sahar__tchannels_createnew_script, name='run_outbrain_Sahar__tchannels_createnew_script'),
    path('run_outbrain_Sahar__tchannelsdb_script/', views.run_outbrain_Sahar__tchannelsdb_script, name='run_outbrain_Sahar__tchannelsdb_script'),

    path('run_Sahar_outbrain_uploader_script/', views.run_Sahar_outbrain_uploader_script, name='run_Sahar_outbrain_uploader_script'),



    path('run_Sahar_tonic_taboolaoffers_script/', views.run_Sahar_tonic_taboolaoffers_script, name='run_Sahar_tonic_taboolaoffers_script'),
    path('run_Sahar_rsoctoniccreateofferestaboola_script/', views.run_Sahar_rsoctoniccreateofferestaboola_script, name='run_Sahar_rsoctoniccreateofferestaboola_script'),

    path('run_Sahar_tabduplicatorfortest_s1_script/', views.run_Sahar_tabduplicatorfortest_s1_script, name='run_Sahar_tabduplicatorfortest_s1_script'),
    path('run_Sahar_tabduplicatorfortest_Inuvo_script/', views.run_Sahar_tabduplicatorfortest_Inuvo_script, name='run_Sahar_tabduplicatorfortest_Inuvo_script'),
    path('run_Sahar_tabduplicatorfortest_AFD_script/', views.run_Sahar_tabduplicatorfortest_AFD_script, name='run_Sahar_tabduplicatorfortest_AFD_script'),
    path('run_Sahar_tabduplicatorfortest_RSOC_script/', views.run_Sahar_tabduplicatorfortest_RSOC_script, name='run_Sahar_tabduplicatorfortest_RSOC_script'),
    path('run_Sahar_tabduplicatorfortest_TC_script/', views.run_Sahar_tabduplicatorfortest_TC_script, name='run_Sahar_tabduplicatorfortest_TC_script'),

    path('run_taboola_Sahar_newpolicycheckforall_script/', views.run_taboola_Sahar_newpolicycheckforall_script, name='run_taboola_Sahar_newpolicycheckforall_script'),


    path('run_taboola_Sahar__tchannels_createnew_script/', views.run_taboola_Sahar__tchannels_createnew_script, name='run_taboola_Sahar__tchannels_createnew_script'),
    path('run_taboola_Sahar__tchannelsdb_script/', views.run_taboola_Sahar__tchannelsdb_script, name='run_taboola_Sahar__tchannelsdb_script'),

    path('run_Sahar_upload_taboola_creatives_S1_script/', views.run_Sahar_upload_taboola_creatives_S1_script, name='run_Sahar_upload_taboola_creatives_S1_script'),
    path('run_Sahar_upload_taboola_creatives_TC_script/', views.run_Sahar_upload_taboola_creatives_TC_script, name='run_Sahar_upload_taboola_creatives_TC_script'),
    path('run_Sahar_upload_taboola_creatives_RSOC_script/', views.run_Sahar_upload_taboola_creatives_RSOC_script, name='run_Sahar_upload_taboola_creatives_RSOC_script'),
    path('run_Sahar_upload_taboola_creatives_Inuvo_script/', views.run_Sahar_upload_taboola_creatives_Inuvo_script, name='run_Sahar_upload_taboola_creatives_Inuvo_script'),

    path('run_Sahar_keywordsanalyze_script/', views.run_Sahar_keywordsanalyze_script, name='run_Sahar_keywordsanalyze_script'),
    path('run_Sahar_keywordstokeywords_v3_script/', views.run_Sahar_keywordstokeywords_v3_script, name='run_Sahar_keywordstokeywords_v3_script'),
    path('run_Sahar_creatives_builder_script/', views.run_Sahar_creatives_builder_script, name='run_Sahar_creatives_builder_script'),

    path('media_buyer_Jenia_page/', views.media_buyer_Jenia_page, name='media_buyer_Jenia_page'),












]
