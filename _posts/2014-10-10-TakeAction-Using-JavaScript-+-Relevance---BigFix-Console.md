#### Note: this post has some formatting issues due to it being pulled from existing HTML.
<div>
<p dir="ltr">
	It is possible to use JavaScript + Relevance within the BigFix Windows Console to customize behavior of Fixlets / Tasks and other content.</p>
<p dir="ltr">
	&nbsp;</p>
<p dir="ltr">
	One example is to prevent the console user from "Taking Action" on a Fixlet or Task, unless certain criteria are met.</p>
<ul dir="ltr">
	<li>
		document.body.ontakeaction
		<ul>
			<li>
				allows JavaScript to be executed when the "Take Action" button is clicked in the console.
				<ul>
					<li>
						Can be used to prevent the "Take Action" from continuing.&nbsp;</li>
				</ul>
			</li>
		</ul>
	</li>
</ul>
<p dir="ltr">
	Some potential use cases for preventing "Take Action" on a Fixlet or Task:</p>
<ul dir="ltr">
	<li>
		Only allow certain users to "Take Action"
		<ul>
			<li>
				Some actions may be managed by a central group and duplicate actions should not be taken by other operators, even if they have read access to the site.</li>
			<li>
				Users could be authorized explicitly, or based upon role, or other criteria.</li>
			<li>
				<strong>if ("NormalUser1" == Relevance('name of current console user') || Relevance('exists current console user whose(master flag of it)'))</strong></li>
			<li>
				<strong>if ( Relevance('(master flag of current console user) OR ( /* Make sure the user has at least one of the roles */ &nbsp;1 is less than or equal to the number of elements of intersections of (set of bes roles whose(name of it = "ROLE1" OR name of it = "ROLE2"); role set of current console user))')&nbsp;)</strong></li>
		</ul>
	</li>
	<li>
		Only allow users that are writers to the site the fixlet resides in to "Take Action"
		<ul>
			<li>
				Example: Template tasks that are not meant to be run directly, but copied and modified by the user before use.</li>
			<li>
				<strong>Relevance('exists writers whose(it = current console user) of site of current fixlet')</strong></li>
		</ul>
	</li>
</ul>
<p dir="ltr">
	&nbsp;</p>
<h2 dir="ltr">
	Full JavaScript + Relevance Example:</h2>
<pre dir="ltr">
document.body.ontakeaction = function() {
	if ( "NormalUser1" == Relevance('name of current console user') || Relevance('(master flag of current console user) OR ( /* Make sure the user has at least one of the roles */ 1 is less than or equal to the number of elements of intersections of (set of bes roles whose(name of it = "ROLE1" OR name of it = "ROLE2"); role set of current console user))') )
	{
		TakeFixletAction( Relevance('id of current fixlet'), Relevance('id of current bes site'), "Action1", {}, {} );
	} else {
		alert( "Only for authorized users, please contact support for assistance." );
	}
	return false;
}
</pre>
<p dir="ltr">
	&nbsp;</p>
<h2 dir="ltr">
	Steps:</h2>
<table border="0" dir="ltr" style="width: 100%;">
	<tbody>
		<tr>
			<td style="width: 58px; text-align: center;">
				1.</td>
			<td style="width: 262px;">
				Create or Edit content</td>
			<td style="width: 531px;">
				<img lconnwikiparamattachmentname="TakeAction_JavaScript_Relevance_1.PNG" src="http://www.ibm.com/developerworks/community/wikis/form/anonymous/api/wiki/90553c0b-42eb-4df0-9556-d3c2e0ac4c52/page/ac74ae17-0874-41b0-b0f4-fe9e757d479f/attachment/399188f8-b35f-4095-99ec-4e3e0b1aae58/media/TakeAction_JavaScript_Relevance_1.PNG" lconnwikiparamwikipage="IEM Console JavaScript + Relevance" lconnwikimacro="image"></img></td>
		</tr>
		<tr>
			<td style="width: 58px; text-align: center;">
				2.</td>
			<td style="width: 262px;">
				Click the add script button</td>
			<td style="width: 531px;">
				<img lconnwikiparamattachmentname="TakeAction_JavaScript_Relevance_1B.png" src="http://www.ibm.com/developerworks/community/wikis/form/anonymous/api/wiki/90553c0b-42eb-4df0-9556-d3c2e0ac4c52/page/ac74ae17-0874-41b0-b0f4-fe9e757d479f/attachment/37f4fa19-017c-4937-acf8-b1e2bf6959f7/media/TakeAction_JavaScript_Relevance_1B.png" lconnwikiparamwikipage="IEM Console JavaScript + Relevance" lconnwikimacro="image"></img></td>
		</tr>
		<tr>
			<td style="width: 58px; text-align: center;">
				3.</td>
			<td style="width: 262px;">
				Paste the JavaScript modified as needed</td>
			<td style="width: 531px;">
				<img lconnwikiparamattachmentname="TakeAction_JavaScript_Relevance_2.PNG" src="http://www.ibm.com/developerworks/community/wikis/form/anonymous/api/wiki/90553c0b-42eb-4df0-9556-d3c2e0ac4c52/page/ac74ae17-0874-41b0-b0f4-fe9e757d479f/attachment/d918b83a-3710-489e-8e8e-fda73feb85e8/media/TakeAction_JavaScript_Relevance_2.PNG" lconnwikiparamwikipage="IEM Console JavaScript + Relevance" lconnwikimacro="image"></img></td>
		</tr>
		<tr>
			<td style="width: 58px; text-align: center;">
				4.</td>
			<td style="width: 262px;">
				Click the "OK" button to save script</td>
			<td style="width: 531px;">
				<img lconnwikiparamattachmentname="TakeAction_JavaScript_Relevance_2B.png" src="http://www.ibm.com/developerworks/community/wikis/form/anonymous/api/wiki/90553c0b-42eb-4df0-9556-d3c2e0ac4c52/page/ac74ae17-0874-41b0-b0f4-fe9e757d479f/attachment/6b92db14-2db0-4579-a211-5af537bc3e6a/media/TakeAction_JavaScript_Relevance_2B.png" lconnwikiparamwikipage="IEM Console JavaScript + Relevance" lconnwikimacro="image"></img></td>
		</tr>
		<tr>
			<td style="width: 58px; text-align: center;">
				5.</td>
			<td style="width: 262px;">
				Make any further changes to the content</td>
			<td style="width: 531px;">
				<img lconnwikiparamattachmentname="TakeAction_JavaScript_Relevance_3.PNG" src="http://www.ibm.com/developerworks/community/wikis/form/anonymous/api/wiki/90553c0b-42eb-4df0-9556-d3c2e0ac4c52/page/ac74ae17-0874-41b0-b0f4-fe9e757d479f/attachment/bad9d5e5-49b6-487a-9193-2631746e0a31/media/TakeAction_JavaScript_Relevance_3.PNG" lconnwikiparamwikipage="IEM Console JavaScript + Relevance" lconnwikimacro="image"></img></td>
		</tr>
		<tr>
			<td style="width: 58px; text-align: center;">
				6.</td>
			<td style="width: 262px;">
				Click the "OK" button to save content</td>
			<td style="width: 531px;">
				<img lconnwikiparamattachmentname="TakeAction_JavaScript_Relevance_3B.png" src="http://www.ibm.com/developerworks/community/wikis/form/anonymous/api/wiki/90553c0b-42eb-4df0-9556-d3c2e0ac4c52/page/ac74ae17-0874-41b0-b0f4-fe9e757d479f/attachment/1aa05e1c-3c9e-4a32-9477-cbe2cf97e540/media/TakeAction_JavaScript_Relevance_3B.png" lconnwikiparamwikipage="IEM Console JavaScript + Relevance" lconnwikimacro="image"></img></td>
		</tr>
	</tbody>
</table>
<p dir="ltr">
	&nbsp;</p>
<p dir="ltr">
	&nbsp;</p>
<h2 dir="ltr">
	References:</h2>
<p dir="ltr">
	<a href="https://www.ibm.com/developerworks/community/forums/html/topic?id=77777777-0000-0000-0000-000014849827">https://www.ibm.com/developerworks/community/forums/html/topic?id=77777777-0000-0000-0000-000014849827</a></p>
<p dir="ltr">
	<a href="http://bigfix.me/relevance/details/2999187">http://bigfix.me/relevance/details/2999187</a></p>
<p dir="ltr">
	<a wiki="Tivoli Endpoint Manager" href="https://www.ibm.com/developerworks/community/wikis/home?lang=en#!/wiki/Tivoli%20Endpoint%20Manager/page/Console%20JavaScript%20Events" id="wikiLink1412951356465" page="Console JavaScript Events">https://www.ibm.com/developerworks/community/wikis/home?lang=en#!/wiki/Tivoli%20Endpoint%20Manager/page/Console%20JavaScript%20Events</a></p>
<p dir="ltr">
	Example:&nbsp;<a href="http://bigfix.me/fixlet/details/3876">http://bigfix.me/fixlet/details/3876</a></p></div>
