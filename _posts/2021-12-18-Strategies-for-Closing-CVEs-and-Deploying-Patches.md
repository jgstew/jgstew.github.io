The best way to close [vulnerabilities (CVEs)](https://github.com/jgstew/jgstew.github.io/blob/master/_posts/2019-08-16-What-makes-a-vulnerability-or-CVE-worse-than-others%3F.md) and deploy patches depends on who you ask. Today the biggest concern may be Log4j CVEs, but this really applies to every patch and every CVE every day.

I am going to present some exaggerated options from different perspectives. 

### Device Owner / Service User

I use a combination of laptop, desktop, or mobile devices to do my job. I want software to be installed whenever I need it for my job or updated when there is a cool new feature available, but only if I know about it and want it or if it is very compelling. I also rely on services provided by internal and external teams. I care more about having access to my data than my data getting leaked, but I also don't want my sensitive data to be leaked.

**Goals:** Never loose productivity due to problems, bugs, or malware, but also never patch, reboot, or change anything unexpectedly. Never loose access to services, and never loose access to my data. I want cool new features to be available immediately.

**Preferred Patching Strategy:** Do not apply patches. Do not reboot my system for me. Don't ever force me to do anything.

**What I loose sleep over:** Loosing data or work I was in the middle of because of a forced reboot or similar change or any other reason. Or just loosing track of what I was working on because of a forced or unexpected disruption.

### Application / Service Owner

I am responsible for a service and applications to provide that service, secondarily encompassing any servers or infrastructure that provides the service. If there is any downtime, my users are mad and let me know it. My end users should never be unhappy due to downtime or any other reason, especially those outside of my control. If my service must be disrupted, then it must be done in the exact unique maintenance window I desire.

**Goals:** 100% uptime, no maintenance windows. All updates are installed and effective instantly with no gaps in service and no reboots. The service I'm responsible for is more critical than all other services. This is also true of any other service I am responsible for if more than one, it is also the most important service.

**Preferred Patching Strategy:** No disruptions, no reboots, no patches, unless there are cool new feature updates available, then please update before the next maintenance window even if it violates my SLA. Any update should be first deployed to a test environment that mirrors the production one in every possible way.

**What I loose sleep over:** Any extended downtime or denial of service or loss of data.

### Security Operations

I am responsible for the overall security of all aspects of the organization. I care most about critical vulnerabilities that can be exploited remotely or allow data exfiltration, but ideally all vulnerabilities should be closed as soon as possible. I care more about data exfiltration than I do about downtime due to restoring data from backups. I care more about closing vulnerabilities than I do service disruptions.

**Goals:** No compromises, No malware, No data exfiltration. Maximum visibility into what is out there.

**Preferred Patching Strategy:** All patches should be installed and effective within 72 hours or less of vendor availability.

**What I loose sleep over:** Today it is Log4j, but tomorrow it will be something new. Even worse is all the old vulnerabilities that are still open that I do not know about, and any unknown ones that are already being exploited that I don't know how to look for yet. It is the amount of things I know I do not know that truly frighten me, and the knowledge that compromises are inevitable even with infinite resources to combat them. 

### IT Operations

I am responsible for keeping device owners, service users, and service owners happy by making sure things are running smoothly and they get new features they ask for in a timely manner, while also trying to keep security operations happy by deploying patches that my device owners and service owners don't want to be bothered by. I am responsible for helping prevent data loss as well as data exfiltration. I am responsible for helping maintain uptime and service agreements, while also doing a job that causes required disruptions.

**Goals:** Keep everyone happy while keeping things simple and streamlined, but also maximizing automation to make it easier to do, which in turn allows me to improve delivery of other aspects of IT Operations. I never want any patch or operation to disrupt anyone, particularly outside of defined maintenance windows.

**Preferred Patching Strategy:** In 72 hours or less, but also never. I want patches to roll out gradually in case they cause unexpected problems, but I also don't want to maintain an infinite number of maintenance windows and exceptions or manually patch systems in unique ways every time.

**What I loose sleep over:** That keeping everyone happy is impossible. That it is possible for a patch to unintentionally cause a service disruption or other downtime, but that not deploying patches in a timely manner leads to compromises, which also leads to service disruption and downtime.

--------

### Well that is unhelpful, what should I do?

It is impossible to keep all parties perfectly happy, which means that compromise is required. The best option is likely to strike a balance and try to have all parties equally unhappy, while also keeping things manageable and automatable. Too much complexity and overhead itself causes problems.

Whatever process you follow today, it is already making some sort of compromise for the benefit of some  groups and the detriment of others because no one has infinite resources. Even if you had infinite resources, you would still have unintended and unexpected problems eventually because perfect uptime, availability, redundancy, and security are not possible.

One option is to map out the current processes and compromises being made today and reexamine them to figure out how you can change, refine, or simplify them to make a different compromise for the future.

Another option is to throw everything out and try to work out from scratch what a realistic ideal is from the perspective of every group individually, and then try to figure out how to come to a new compromise that tries to make every party equally happy and unhappy in balance with the others.

If your organization is unique and needs higher assurances of uptime or security or both, then that means you need more resources and focus to make that a reality, which you still won't be able to do perfectly or always have enough resources to do, so you will still need to make compromises.

Sometimes the real issue is that the required compromises are hidden, inconsistent, or not clearly communicated. Sometimes a less than ideal compromise that is clearly communicated is better than a more ideal compromise that is not communicated.

--------

### Related:

- https://www.jgstew.com/bigfix/2019/08/16/What-makes-a-vulnerability-or-CVE-worse-than-others.html
- https://forum.bigfix.com/t/log4j-cve-2021-44228-cve-2021-45046-summary-page/40222/9
- https://forum.bigfix.com/t/log4j-cve-2021-44228-detection-and-mitigation/40141
- https://forum.bigfix.com/t/working-to-detect-and-remove-the-edellroot-malicious-root-certificate/15089
