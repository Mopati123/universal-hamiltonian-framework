#!/usr/bin/env python3
"""
Quick-Start Example: Deploy Multi-Agent System

Run this to immediately generate business plans for all 10 SaaS applications.

Usage:
    python quickstart.py                    # Uses default (hybrid mode)
    python quickstart.py --mode parallel    # All agents parallel (fastest)
    python quickstart.py --mode sequential  # Sequential (best coordination)
    python quickstart.py --agents 3         # Deploy only 3 agents (for testing)
    python quickstart.py --commit           # Write outputs after commit gate
"""

import asyncio
import sys
import argparse
from agents import GovernorAI, SaaSType


async def main():
    parser = argparse.ArgumentParser(description="Deploy Multi-Agent SaaS Business Plan System")
    parser.add_argument("--mode", choices=["parallel", "sequential", "hybrid"], 
                       default="hybrid", help="Deployment mode")
    parser.add_argument("--agents", type=int, default=10, 
                       help="Number of agents to deploy (1-10)")
    parser.add_argument("--output", default="./saas_business_plans", 
                       help="Output directory")
    parser.add_argument("--commit", action="store_true",
                       help="Write outputs only after approval gates pass")
    parser.add_argument("--min-quality", type=float, default=75.0,
                       help="Minimum quality threshold for commit approval")
    parser.add_argument("--allow-template-commit", action="store_true",
                       help="Allow template outputs to pass commit gate")
    
    args = parser.parse_args()
    
    # Validate agent count
    if not 1 <= args.agents <= 10:
        print(f"❌ Error: Must deploy 1-10 agents, got {args.agents}")
        sys.exit(1)
    
    # Create Governor
    print("\n" + "="*80)
    print("🤖 MULTI-AGENT SAAS BUSINESS PLAN SYSTEM")
    print("="*80)
    print(f"Mode: {args.mode.upper()}")
    print(f"Agents: {args.agents}/10")
    print(f"Output: {args.output}")
    print("="*80 + "\n")
    
    governor = GovernorAI(quality_threshold=args.min_quality)
    
    # Optionally filter agents
    if args.agents < 10:
        saas_types = list(SaaSType)[:args.agents]
        governor.agents = {
            st.name: governor.agents[st.name] 
            for st in saas_types if st.name in governor.agents
        }
        print(f"⚠️  Deploying {args.agents} agents for testing:\n")
        for agent_name in governor.agents.keys():
            print(f"   • {agent_name}")
        print()
    
    # Deploy agents
    print(f"[{args.mode.upper()}] Deploying agents...\n")
    await governor.deploy_all_agents(mode=args.mode)
    
    # Quality control
    print("\n")
    qc_report = governor.quality_control()
    
    # Executive summary
    print("\n")
    summary = governor.generate_executive_summary()
    
    # Commit outputs only after approval
    print("\n")
    approved = governor.authorize_commit(
        min_quality=args.min_quality,
        allow_template_commit=args.allow_template_commit,
    )
    artifacts_written = []
    committed = False
    if args.commit and approved:
        artifacts_written = governor.save_all_outputs(args.output, commit=True)
        committed = bool(artifacts_written)
    elif args.commit:
        print("Outputs were not committed. Fix QC issues or allow template commits.")
    else:
        print("Dry run only. Re-run with --commit to write outputs.")

    manifest = governor.build_run_manifest(
        mode=args.mode,
        agents_executed=list(governor.agents.keys()),
        commit_requested=args.commit,
        commit_approved=approved,
        artifacts_written=artifacts_written,
    )
    manifest_path = governor.write_run_manifest(args.output, manifest)
    print(f"Run manifest: {manifest_path}")
    
    # Final report
    print("\n" + "="*80)
    print("✅ EXECUTION COMPLETE")
    print("="*80)
    status = governor.get_status_report()
    print(f"Completed: {status['completed']}/{status['total_agents']} agents")
    print(f"Quality:   {status['average_quality']:.1f}%")
    if committed:
        print(f"Output:    {args.output}/")
        print("\nNext steps:")
        print(f"  1. Review: {args.output}/GOVERNOR_EXECUTIVE_SUMMARY.json")
        print(f"  2. Review: {args.output}/run_manifest.json")
        print(f"  3. Read:  {args.output}/[SaaSType]/deliverables.json")
    else:
        print("Output:    not committed")
        print("\nNext steps:")
        print(f"  1. Review: {args.output}/run_manifest.json")
        print("  2. Re-run with --commit after fixing QC issues")
    print("="*80 + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n❌ Execution cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
