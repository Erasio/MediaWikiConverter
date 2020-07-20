class Tests:

    shortTest = """[[Category:Meta]]
The wiki thrives off of its users and their contributions. 

Only with ''your'' help can we keep everything up to date and as useful as possible for everyone! 



== How can you contribute ==

Everyone is able to edit and create pages! You don't need to sign up for an account either! Don't be afraid to start editing or creating a new page right now! 

You can find out more about how to write wiki articles [https://www.mediawiki.org/wiki/Help:Formatting over here on the wikimedia formatting page] and [https://www.ue4community.wiki/Wiki_Style_Guide over here for your own style guide]

If you're working on something that's not ready yet just leave it out of any categories and use the draft template by writing <pre>{{draft}}</pre> 

In the beginning you might see that your page has been sent to the moderators for review. This is exclusively meant to prevent spam and malicious edits. We will approve every serious contribution usually within 24 hours. You can keep making changes to a page in the moderation queue. After 10 approved edits and 7 days after your registration you can avoid the moderation queue entirely.

Should you see outdated content, inappropriate behavior, technical issues or have feature requests check out [https://forms.gle/ZCkEj33YqWuSwvzX9 this form]!

If you have any questions about how you can help please come visit our [https://discord.com/invite/GCkCcxP wiki discord]!

We're always happy to see new faces!"""
        

    complexTest = """<div style="float:right; padding-left: 2pt;">__TOC__</div>

{{draft}}
{{ContextSwitch}}

[[Category:C++]]
[[Category:Blueprint]]
[[Category:Concepts]]

== Introduction ==
Actor is one of the most important aspects of Unreal Engine, it lays at the core of everything you will do interacting in the Unreal Editor viewport and the Game World. This core Unreal Engine Class {{code|AActor}} forms the basis for any Object you can see in the viewport in the 3d space, this does not include UMG widgets which are overlays.

=== Components ===
Actors are made up of various [[Component|Components]].

=== Info ===
There are a class of Actors which have very minimal presence in the game world, they are largely managers and extend from the {{code|Info}} Actor. See [[Game Framework explained]] for more.

== Spawn ==
Spawning refers to the process of creating an Actor, similar to New Object though having a physical presence in the game world means Actors are treated differently, because they have components like collision. If an Actors Spawn location is being blocked we call that Encroachment, its when two Actors (or more) share the same physical space.
<div id="CPP" class="context-panel" style="display:block">
<syntaxhighlight lang="C++">GetWorld()->SpawnActor<AYourActor>();</syntaxhighlight>

Since there is a requirement to having a game world we must first {{code|GetWorld}} to call Spawn on, this function is inherited by all Actors. This is the most basic implementation calling the default constructor.

<syntaxhighlight lang="C++">
    FActorSpawnParameters SpawnInfo;
    SpawnInfo.Owner = this;
    SpawnInfo.Instigator = GetInstigator();
    SpawnInfo.ObjectFlags |= RF_Transient;
    YourActorReference = GetWorld()->SpawnActor<AYourActor>(SpawnInfo);
</syntaxhighlight>
Spawning has the associated structure {{code|FActorSpawnParameters}} which is used to pass in a number of parameters to the Spawn function as in this example.

<syntaxhighlight lang="C++">GetWorld()->SpawnActor<AYourActor>(YourActorClass, SpawnInfo);</syntaxhighlight>
The above lets you specify a class with {{code|YourActorClass}} you may wish this to be editable on children of this class.

{{epic|https://docs.unrealengine.com/en-US/API/Runtime/Engine/Engine/UWorld/SpawnActor/index.html Spawn Actor API}}
{{epic|https://docs.unrealengine.com/en-US/Programming/UnrealArchitecture/Actors/Spawning/index.html Spawning Actors in C++}}
</div><div id="BP" class="context-panel" style="display:none">
{{epic|https://docs.unrealengine.com/en-US/Gameplay/HowTo/SpawnAndDestroyActors/Blueprints/index.html Spawning and Destroying Actors in Blueprint}}
</div>
=== Owner ===
{{todo|GetOwner()}}

== Destroy ==
If you are finished with an Actor simply call the {{code|Destroy}} method.
<div id="CPP" class="context-panel" style="display:block">
<syntaxhighlight lang="C++">YourActor->Destroy();</syntaxhighlight>
</div><div id="BP" class="context-panel" style="display:none">
</div>
{{todo|can bind delegates to spawn/destroy events}}
== Archetypes ==
<div id="CPP" class="context-panel" style="display:block">
This structure {{code|FActorSpawnParameters}} gives us an opportunity to use another existing Actor as a Template for spawning, as shown below with {{code|YourTemplateActor}} reference being set to use when Spawned.
<syntaxhighlight lang="C++">
    FActorSpawnParameters SpawnInfo;
    SpawnInfo.Owner = this;
    SpawnInfo.Template = YourTemplateActor;
    YourActorReference = GetWorld()->SpawnActor<AYourActor>(SpawnInfo);
</syntaxhighlight>
{{epic|https://docs.unrealengine.com/en-US/API/Runtime/Engine/Engine/FActorSpawnParameters/index.html FActorSpawnParameters}}
</div>
== Attachment ==
<div id="CPP" class="context-panel" style="display:block">
Attaching Actors typically happens through their Components, the most basic form of attachment would be through two Actors Root Components using {{code|AttachToActor}}.
<syntaxhighlight lang="C++">AttachToActor(ParentActor);</syntaxhighlight>

You can also optionally use the named socket or FAttachmentTransformRules.
<syntaxhighlight lang="C++">AttachToActor(ParentActor, FAttachmentTransformRules, SocketName);</syntaxhighlight>

<syntaxhighlight lang="C++">AttachToComponent(USceneComponent * Parent, FAttachmentTransformRules, SocketName);</syntaxhighlight>

To check to see if your attachment worked.
<syntaxhighlight lang="C++">if(YourActor->IsAttachedTo(ParentActor)){}</syntaxhighlight>

<syntaxhighlight lang="C++">USceneComponent* AttachComponent = YourActor->GetDefaultAttachComponent();</syntaxhighlight>

<syntaxhighlight lang="C++">TArray <AActor*> YourOutActors,
YourActor->GetAttachedActors(&YourOutActors, false);</syntaxhighlight>

{{code|YourOutActors}} array is now filled with a list of all Actors attached to {{code|YourActor}}.

<syntaxhighlight lang="C++">ParentActor = YourActor->GetAttachParentActor();</syntaxhighlight>

=== Detachment ===
<syntaxhighlight lang="C++">YourActor->DetachFromActor(FDetachmentTransformRules);</syntaxhighlight>
Detaches the RootComponent of this Actor from any SceneComponent it is currently attached to.

<syntaxhighlight lang="C++">YourActor->DetachAllSceneComponents(ParentComponent, FDetachmentTransformRules);</syntaxhighlight>

=== Sockets ===
<syntaxhighlight lang="C++">FName    GetAttachParentSocketName()</syntaxhighlight>

=== Editor === 
<syntaxhighlight lang="C++">FText* Reason = "";
if(YourActor->EditorCanAttachTo(YourParent, Reason){}</syntaxhighlight>

</div>
== Replication ==
=== Actor Channels ===

== Further Reading ==
{{epic|https://docs.unrealengine.com/en-US/Programming/UnrealArchitecture/Actors/index.html Actors Architecture}}
<div id="CPP" class="context-panel" style="display:block">
{{epic|https://docs.unrealengine.com/en-US/API/Runtime/Engine/GameFramework/AActor/index.html Actor API}}
</div><div id="BP" class="context-panel" style="display:none">
{{epic|https://docs.unrealengine.com/en-US/Engine/Actors/index.html Using Actors in Unreal Editor}}
{{epic|https://docs.unrealengine.com/en-US/Engine/Blueprints/BP_HowTo/ActorReference/index.html Actor References in Blueprint}}
{{epic|https://docs.unrealengine.com/en-US/BlueprintAPI/Actor/index.html Actor}}
</div>
"""
