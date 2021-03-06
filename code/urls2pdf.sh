#!/bin/sh

css=file:///data/temp/fetchf5exam1/a.css
log=$(pwd)/wk.log
outputdir=$(pwd)/outputs

mkdir -p $outputdir

url2pdf(){
  echo "processing # $2 $1" | tee -a $log
  wkhtmltopdf --user-style-sheet $css $1 "$outputdir/$2.pdf" &
}

i=1
j=10

for uri in $(cat $1);do

  url2pdf $uri $i
  i=$((i+1))

  [ $( expr $i % $j ) -eq 0 ] && sleep 60

done
#pdfunite *.pdf urls.pdf
#http://www.briefmenow.org/f5/how-many-distinct-virtual-servers-does-the-client-conne/
#http://www.briefmenow.org/f5/which-configuration-change-resolves-this-problem-2/
#http://www.briefmenow.org/f5/why-are-users-unable-to-connect-directly-to-the-applica/
#http://www.briefmenow.org/f5/which-url-should-be-reported-to-the-serverapplication/
#http://www.briefmenow.org/f5/what-caused-the-failover/
#http://www.briefmenow.org/f5/which-modification-will-allow-the-ltm-device-to-process/
#http://www.briefmenow.org/f5/which-configuration-change-resolves-this-problem/
#http://www.briefmenow.org/f5/what-should-the-ltm-specialist-do-to-resolve-the-issue/
#http://www.briefmenow.org/f5/what-should-the-ltm-specialist-do-to-fix-this-issue/
#http://www.briefmenow.org/f5/what-should-the-ltm-specialist-configure-to-allow-the-i/
#http://www.briefmenow.org/f5/what-should-the-administrator-do-to-correct-the-problem/
#http://www.briefmenow.org/f5/which-configuration-change-will-allow-the-application-t/
#http://www.briefmenow.org/f5/what-is-the-root-cause-of-the-problem-3/
#http://www.briefmenow.org/f5/what-is-the-issue-10/
#http://www.briefmenow.org/f5/what-is-the-cause-of-the-application-access-problem/
#http://www.briefmenow.org/f5/what-is-the-problem-with-the-images-loading-through-the/
#http://www.briefmenow.org/f5/what-is-the-problem-with-the-configuration-on-the-ltm-d/
#http://www.briefmenow.org/f5/how-should-the-ltm-specialist-fix-the-issue/
#http://www.briefmenow.org/f5/how-should-the-ltm-specialist-modify-the-configuration/
#http://www.briefmenow.org/f5/which-two-servers-are-missing-two-frequently-used-urls/
#http://www.briefmenow.org/f5/which-server-is-causing-the-highest-latency-for-users/
#http://www.briefmenow.org/f5/what-should-the-ltm-specialist-do-to-resolve-this-issue/
#http://www.briefmenow.org/f5/which-solution-has-the-simplest-configuration-changes-w/
#http://www.briefmenow.org/f5/how-should-the-ltm-specialist-minimize-the-configuration/
#http://www.briefmenow.org/f5/how-many-unique-monitors-remain/
#http://www.briefmenow.org/f5/a-pair-of-ltm-devices-is-configured-for-h/
#http://www.briefmenow.org/f5/what-triggered-the-ltm-device-failover/
#http://www.briefmenow.org/f5/where-should-the-ltm-specialist-check-for-potential-issues/
#http://www.briefmenow.org/f5/what-is-the-issue-9/
#http://www.briefmenow.org/f5/what-does-the-output-mean/
#http://www.briefmenow.org/f5/which-two-solutions-will-solve-the-configuration-problem/
#http://www.briefmenow.org/f5/which-change-to-the-ltm-device-configuration-will-resol/
#http://www.briefmenow.org/f5/what-is-the-problem-5/
#http://www.briefmenow.org/f5/what-is-the-root-cause-of-the-problem-2/
#http://www.briefmenow.org/f5/what-is-the-root-cause-of-the-error/
#http://www.briefmenow.org/f5/what-is-the-solution-to-the-problem-2/
#http://www.briefmenow.org/f5/what-is-the-solution-to-the-problem/
#http://www.briefmenow.org/f5/how-should-the-ltm-specialist-modify-the-http-profile-t/
#http://www.briefmenow.org/f5/what-is-the-cause-of-the-failure/
#http://www.briefmenow.org/f5/how-should-the-send-string-be-modified-to-correct-this/
#http://www.briefmenow.org/f5/what-is-the-root-cause-of-the-problem/
#http://www.briefmenow.org/f5/what-is-the-issue-8/
#http://www.briefmenow.org/f5/what-is-the-issue-7/
#http://www.briefmenow.org/f5/what-is-the-cause-of-the-issue/
#http://www.briefmenow.org/f5/what-is-the-issue-6/
#http://www.briefmenow.org/f5/what-is-the-issue-5/
#http://www.briefmenow.org/f5/which-configuration-should-the-ltm-specialist-modify-to/
#http://www.briefmenow.org/f5/which-step-should-an-ltm-specialist-take-to-utilize-avr/
#http://www.briefmenow.org/f5/what-is-the-solution/
#http://www.briefmenow.org/f5/how-should-the-ltm-specialist-resolve-this-issue-5/
#http://www.briefmenow.org/f5/what-is-the-issue-4/
#http://www.briefmenow.org/f5/what-is-the-issue-3/
#http://www.briefmenow.org/f5/which-two-locations-could-the-packet-capture-have-been-2/
#http://www.briefmenow.org/f5/which-tcpdump-filter-will-help-trace-the-monitor/
#http://www.briefmenow.org/f5/which-two-actions-will-resolve-the-problem/
#http://www.briefmenow.org/f5/why-is-the-server-returning-this-error/
#http://www.briefmenow.org/f5/what-is-the-issue-with-the-application/
#http://www.briefmenow.org/f5/which-change-will-resolve-the-problem/
#http://www.briefmenow.org/f5/how-should-this-be-resolved/
#http://www.briefmenow.org/f5/how-soon-after-the-persistence-table-query-was-run-can/
#http://www.briefmenow.org/f5/what-is-the-problem-4/
#http://www.briefmenow.org/f5/where-is-the-reset-originating/
#http://www.briefmenow.org/f5/why-does-the-ip-address-of-101231712-fail-to-appear/
#http://www.briefmenow.org/f5/why-is-there-no-record-of-port-1990-in-the-tcpdump/
#http://www.briefmenow.org/f5/what-is-causing-the-intermittent-issues/
#http://www.briefmenow.org/f5/what-is-the-problem-3/
#http://www.briefmenow.org/f5/what-is-the-problem-2/
#http://www.briefmenow.org/f5/which-step-should-an-ltm-specialist-take-next-to-finish/
#http://www.briefmenow.org/f5/what-is-the-correct-procedure-to-comply-with-the-recomm/
#http://www.briefmenow.org/f5/which-procedure-resolves-the-problem/
#http://www.briefmenow.org/f5/which-device-should-be-upgraded-first/
#http://www.briefmenow.org/f5/which-profile-could-be-removed-or-changed-on-this-virtu/
#http://www.briefmenow.org/f5/which-pool-can-be-removed-without-affecting-client-traffic/
#http://www.briefmenow.org/f5/which-two-items-can-be-consolidated-to-simplify-the-ltm/
#http://www.briefmenow.org/f5/which-objects-in-order-can-be-removed-from-the-partition/
#http://www.briefmenow.org/f5/which-two-actions-should-the-ltm-specialist-perform-to/
#http://www.briefmenow.org/f5/what-is-the-root-cause-of-this-problem/
#http://www.briefmenow.org/f5/what-is-the-cause-of-the-failover-2/
#http://www.briefmenow.org/f5/why-is-the-ltm-specialist-on-ltm-d-unable-to-synchroniz/
#http://www.briefmenow.org/f5/which-two-configuration-components-caused-this-condition/
#http://www.briefmenow.org/f5/which-two-steps-should-the-ltm-specialist-take-to-ident/
#http://www.briefmenow.org/f5/what-are-two-reasons-the-synchronization-group-is-havin/
#http://www.briefmenow.org/f5/what-should-be-added-to-the-configuration-to-resolve-th/
#http://www.briefmenow.org/f5/what-is-the-cause-of-the-failover/
#http://www.briefmenow.org/f5/which-issue-caused-the-failover/
#http://www.briefmenow.org/f5/how-is-the-peer-unit-able-to-determine-the-active-unit/
#http://www.briefmenow.org/f5/what-would-cause-this-behavior/
#http://www.briefmenow.org/f5/which-daemon-failed/
#http://www.briefmenow.org/f5/which-two-actions-would-help-determine-the-cause-of-the/
#http://www.briefmenow.org/f5/which-two-items-could-have-caused-the-failover-event/
#http://www.briefmenow.org/f5/which-command-should-the-ltm-specialist-run-through-ssh/
#http://www.briefmenow.org/f5/which-command-should-the-ltm-specialist-use-to-determin/
#http://www.briefmenow.org/f5/which-http-profile-setting-can-be-modified-temporarily/
#http://www.briefmenow.org/f5/which-command-should-be-executed-to-verify-the-ltm-devi/
#http://www.briefmenow.org/f5/which-command-should-be-executed-on-the-command-line-in/
#http://www.briefmenow.org/f5/how-should-the-ltm-specialist-check-the-radius-server-a/
#http://www.briefmenow.org/f5/which-command-determines-the-current-baud-rate-via-the/
#http://www.briefmenow.org/f5/which-command-is-used-to-produce-this-output/
#http://www.briefmenow.org/f5/which-command-was-executed-on-the-ltm-device-to-show-th/
#http://www.briefmenow.org/f5/which-command-should-the-ltm-specialist-execute-on-the-5/
#http://www.briefmenow.org/f5/which-two-subsystems-could-the-ltm-specialist-utilize-t/
#http://www.briefmenow.org/f5/which-command-line-interface-command-will-check-if-the/
#http://www.briefmenow.org/f5/which-command-should-an-ltm-specialist-use-on-the-comma/
#http://www.briefmenow.org/f5/which-command-will-identify-the-active-ltm-device-curre/
#http://www.briefmenow.org/f5/which-command-does-the-ltm-specialist-need-to-run-to-ac/
#http://www.briefmenow.org/f5/which-configuration-item-should-the-ltm-specialist-revi/
#http://www.briefmenow.org/f5/which-two-methods-should-the-ltm-specialist-use-to-conf/
#http://www.briefmenow.org/f5/which-two-commands-should-be-used-to-obtain-additional/
#http://www.briefmenow.org/f5/which-command-should-the-ltm-specialist-use-to-prevent/
#http://www.briefmenow.org/f5/where-would-the-error-message-be-visible-if-one-of-the/
#http://www.briefmenow.org/f5/which-condition-will-trigger-this-log-entry/
#http://www.briefmenow.org/f5/how-should-the-ltm-specialist-resolve-this-issue-4/
#http://www.briefmenow.org/f5/what-is-the-issue-2/
#http://www.briefmenow.org/f5/how-should-the-ltm-specialist-resolve-this-issue-3/
#http://www.briefmenow.org/f5/how-should-the-ltm-specialist-resolve-this-issue-2/
#http://www.briefmenow.org/f5/how-should-the-ltm-specialist-resolve-this-issue/
#http://www.briefmenow.org/f5/what-should-the-ltm-specialist-do-to-solve-the-problem/
#http://www.briefmenow.org/f5/what-is-the-solution-to-this-issue/
#http://www.briefmenow.org/f5/which-http-header-should-the-ltm-specialist-remove-from/
#http://www.briefmenow.org/f5/which-header-field-is-contributing-to-the-issue/
#http://www.briefmenow.org/f5/what-issue-is-the-ltm-specialist-experiencing/
#http://www.briefmenow.org/f5/which-issue-is-the-pool-member-having/
#http://www.briefmenow.org/f5/why-was-the-second-client-flow-permitted-by-the-web-server/
#http://www.briefmenow.org/f5/what-is-the-reason-the-destination-web-server-is-sendin/
#http://www.briefmenow.org/f5/why-is-the-http-web-server-responding-with-a-http-400-b/
#http://www.briefmenow.org/f5/which-two-http-headers-should-be-used-in-sending-the-cl/
#http://www.briefmenow.org/f5/which-header-should-be-used-to-notify-the-clients-brow/
#http://www.briefmenow.org/f5/which-http-header-will-accomplish-this/
#http://www.briefmenow.org/f5/which-http-header-will-supply-this-information-2/
#http://www.briefmenow.org/f5/which-http-header-will-supply-this-information/
#http://www.briefmenow.org/f5/which-three-http-headers-allow-an-application-server-to/
#http://www.briefmenow.org/f5/which-functionality-does-the-irule-provide/
#http://www.briefmenow.org/f5/which-pool-will-be-selected-by-the-irule/
#http://www.briefmenow.org/f5/what-do-the-following-irule-commands-do-when-they-are-u/
#http://www.briefmenow.org/f5/what-does-the-following-irule-do/
#http://www.briefmenow.org/f5/what-is-the-effect-of-an-irule-error-such-as-referencin/
#http://www.briefmenow.org/f5/which-irule-statement-demotes-a-virtual-server-from-cmp/
#http://www.briefmenow.org/f5/which-three-pieces-of-information-does-the-ltm-speciali/
#http://www.briefmenow.org/f5/which-directory-should-the-ltm-specialist-upload-the-script/
#http://www.briefmenow.org/f5/which-monitor-option-should-the-ltm-specialist-enable-o/
#http://www.briefmenow.org/f5/how-does-the-ltm-device-mark-the-monitor-status/
#http://www.briefmenow.org/f5/which-send-string-settings-should-the-ltm-specialist-us/
#http://www.briefmenow.org/f5/how-are-monitored-ltm-device-objects-marked-when-the-bi/
#http://www.briefmenow.org/f5/which-two-configurations-could-an-ltm-specialist-implem/
#http://www.briefmenow.org/f5/which-monitor-should-the-ltm-specialist-configure-to-ve/
#http://www.briefmenow.org/f5/what-should-the-ltm-specialist-enable-to-prevent-the-se/
#http://www.briefmenow.org/f5/what-would-cause-the-pool-members-to-be-marked-down/
#http://www.briefmenow.org/f5/what-is-the-issue/
#http://www.briefmenow.org/f5/which-action-will-resolve-the-problem/
#http://www.briefmenow.org/f5/the-monitor-configuration-is-ltm-monitor-http-common/
#http://www.briefmenow.org/f5/which-two-locations-could-the-packet-capture-have-been/
#http://www.briefmenow.org/f5/which-two-additional-locations-should-protocol-analyzer/
#http://www.briefmenow.org/f5/which-options-will-trace-this-issue/
#http://www.briefmenow.org/f5/which-solution-is-most-efficient-for-obtaining-packet-c/
#http://www.briefmenow.org/f5/which-location-should-the-ltm-specialist-put-a-traffic/
#http://www.briefmenow.org/f5/which-two-locations-are-most-appropriate-to-gather-pack/
#http://www.briefmenow.org/f5/which-two-locations-are-most-appropriate-to-collect-add/
#http://www.briefmenow.org/f5/what-is-causing-the-ssh-connections-to-terminate/
#http://www.briefmenow.org/f5/which-configuration-option-will-result-in-the-desired-b/
#http://www.briefmenow.org/f5/what-should-the-ltm-specialist-do-to-resolve-the-problem/
#http://www.briefmenow.org/f5/which-option-within-the-fastl4-profile-needs-to-be-enab/
#http://www.briefmenow.org/f5/what-should-the-ltm-specialist-do-to-resolve-this/
#http://www.briefmenow.org/f5/why-is-oneconnect-functioning-incorrectly/
#http://www.briefmenow.org/f5/how-should-an-ltm-specialist-determine-if-snat-is-enabl/
#http://www.briefmenow.org/f5/why-are-there-no-errors-for-the-remote-syslog-server-in/
#http://www.briefmenow.org/f5/what-is-the-problem/
#http://www.briefmenow.org/f5/what-should-the-ltm-specialist-use-to-troubleshoot-this/
#http://www.briefmenow.org/f5/which-packet-capture-should-the-ltm-specialist-perform-2/
#http://www.briefmenow.org/f5/which-command-should-the-ltm-specialist-execute-on-the-4/
#http://www.briefmenow.org/f5/why-is-ssldump-failing-to-decrypt-the-application-data/
#http://www.briefmenow.org/f5/which-two-ssl-record-message-details-will-the-ssldump-u/
#http://www.briefmenow.org/f5/which-packet-capture-should-the-ltm-specialist-perform/
#http://www.briefmenow.org/f5/which-command-should-the-ltm-specialist-execute-on-the-3/
#http://www.briefmenow.org/f5/which-two-tools-should-the-ltm-specialist-use-to-troubl/
#http://www.briefmenow.org/f5/which-command-should-the-ltm-specialist-execute-on-the-2/
#http://www.briefmenow.org/f5/which-steps-should-the-ltm-specialist-take-to-capture-t/
#http://www.briefmenow.org/f5/which-command-should-the-ltm-specialist-execute-to-decr/
#http://www.briefmenow.org/f5/which-command-should-the-ltm-specialist-execute-on-the/
#http://www.briefmenow.org/f5/which-irule-will-reject-any-connection-originating-from/
#http://www.briefmenow.org/f5/which-irule-provides-the-proper-functionality/
#http://www.briefmenow.org/f5/which-irule-should-be-used/
#http://www.briefmenow.org/f5/which-irule-should-the-ltm-specialist-use-to-fulfill-th/
#http://www.briefmenow.org/f5/which-irule-will-instruct-the-clients-browser-to-avoid/
#http://www.briefmenow.org/f5/which-irule-will-allow-clients-referencing-wwwexample/
#http://www.briefmenow.org/f5/which-traffic-management-os-alert-level-provides-the-mo/
#http://www.briefmenow.org/f5/which-command-line-tool-should-the-ltm-specialist-use-t/
#http://www.briefmenow.org/f5/which-file-should-be-modified-to-create-custom-snmp-alerts/
#http://www.briefmenow.org/f5/which-two-items-can-be-logged-by-the-application-visibi/
#http://www.briefmenow.org/f5/what-is-a-benefit-provided-by-f5-enterprise-manager/
#http://www.briefmenow.org/f5/which-two-alerting-capabilities-can-be-enabled-from-wit/
#http://www.briefmenow.org/f5/what-is-the-correct-procedure-to-ensure-that-the-instal/
#http://www.briefmenow.org/f5/which-file-would-the-ltm-specialist-find-virtual-server/
#http://www.briefmenow.org/f5/what-is-the-correct-command-to-reset-an-ltm-device-to-i/
#http://www.briefmenow.org/f5/which-two-non-specific-dsc-settings-should-the-ltm-spec/
#http://www.briefmenow.org/f5/what-should-the-ltm-specialist-verify/
#http://www.briefmenow.org/f5/which-three-objects-in-the-virtual-server-configuration/
#http://www.briefmenow.org/f5/what-should-the-ltm-specialist-do-to-reduce-the-number/
#http://www.briefmenow.org/f5/which-two-tcp-profile-settings-should-be-modified-to-co/
#http://www.briefmenow.org/f5/which-built-in-client-side-tcp-profile-provides-the-hig-2/
#http://www.briefmenow.org/f5/which-built-in-client-side-tcp-profile-provides-the-hig/
#http://www.briefmenow.org/f5/which-setting-in-the-udp-profile-will-make-the-ltm-devi/
#http://www.briefmenow.org/f5/which-setting-in-the-tcp-profile-should-reduce-the-amou/
#http://www.briefmenow.org/f5/which-oneconnect-profile-source-mask-should-the-ltm-spe/
