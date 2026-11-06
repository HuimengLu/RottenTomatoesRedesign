const assetPathPrefix = "https://www.figma.com/api/mcp/asset/none";

export default function Filters() {
  return (
    <div className="content-stretch flex items-center justify-between relative size-full" data-node-id="187:369" data-name="Filters">
      <div className="bg-[rgba(255,255,255,0.06)] content-stretch flex gap-[2px] items-start relative rounded-[10px] shrink-0" data-node-id="187:370" data-name="Container">
        <div className="bg-[rgba(255,255,255,0.92)] border border-[rgba(0,0,0,0.2)] border-solid content-stretch flex h-[32px] items-center px-[14px] relative rounded-[8px] shadow-[0px_4px_4px_0px_rgba(0,0,0,0.1)] shrink-0" data-node-id="187:371" data-name="Container">
          <p className="[word-break:break-word] font-['Arial:Bold'] leading-[16px] not-italic relative shrink-0 text-[#1b1c2a] text-[14px] whitespace-nowrap" data-node-id="187:372">
            Top Critics
          </p>
        </div>
        <div className="content-stretch flex h-[32px] items-center px-[14px] relative rounded-[8px] shrink-0" data-node-id="187:373" data-name="Container">
          <p className="[word-break:break-word] font-['Arial:Bold'] leading-[16px] not-italic relative shrink-0 text-[14px] text-[rgba(255,255,255,0.6)] whitespace-nowrap" data-node-id="187:374">
            Fresh
          </p>
        </div>
        <div className="content-stretch flex h-[32px] items-center px-[14px] relative rounded-[8px] shrink-0" data-node-id="187:375" data-name="Container">
          <p className="[word-break:break-word] font-['Arial:Bold'] leading-[16px] not-italic relative shrink-0 text-[14px] text-[rgba(255,255,255,0.6)] whitespace-nowrap" data-node-id="187:376">
            Rotten
          </p>
        </div>
      </div>
    </div>
  );
}
